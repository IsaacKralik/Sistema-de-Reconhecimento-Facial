import tkinter as tk
from tkinter import messagebox
import cv2
import mediapipe as mp
import numpy as np
import os
from PIL import Image, ImageTk
import time
import sqlite3
import pickle

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reconhecimento Facial")
        self.root.geometry("400x180")
        
        self.username = tk.StringVar()
        self.frame_main = tk.Frame(root)
        self.frame_login = tk.Frame(root)
        self.frame_register = tk.Frame(root)
        
        self.setup_main_frame()
        self.setup_login_frame()
        self.setup_register_frame()
        
        self.show_frame(self.frame_main)
        
        # Inicializar variáveis do MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Configurar pasta de referência e banco de dados
        self.reference_folder = "C:\\Users\\Isaac Ribeiro\\Desktop\\Comparador"
        self.db_path = os.path.join(self.reference_folder, "face_recognition.db")
        
        # Inicializar banco de dados e carregar referências
        self.init_database()
        self.reference_data = self.load_references_from_db()

    def setup_main_frame(self):
        tk.Label(self.frame_main, text="Escolha uma opção:").pack(pady=20)
        tk.Button(self.frame_main, text="Login", command=lambda: self.show_frame(self.frame_login)).pack(pady=10)
        tk.Button(self.frame_main, text="Cadastrar", command=lambda: self.show_frame(self.frame_register)).pack()

    def setup_login_frame(self):
        tk.Label(self.frame_login, text="Nome de Usuário:").pack(pady=10)
        tk.Entry(self.frame_login, textvariable=self.username).pack()
        tk.Button(self.frame_login, text="Login", command=self.start_recognition).pack(pady=20)
        tk.Button(self.frame_login, text="Voltar", command=lambda: self.show_frame(self.frame_main)).pack()

    def setup_register_frame(self):
        self.register_name = tk.StringVar()
        tk.Label(self.frame_register, text="Nome para Cadastro:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.register_name).pack()
        tk.Button(self.frame_register, text="Iniciar Cadastro", command=self.start_registration).pack(pady=20)
        tk.Button(self.frame_register, text="Voltar", command=lambda: self.show_frame(self.frame_main)).pack()

    def show_frame(self, frame):
        self.frame_main.pack_forget()
        self.frame_login.pack_forget()
        self.frame_register.pack_forget()
        frame.pack()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS faces
        (id TEXT PRIMARY KEY,
         name TEXT NOT NULL,
         landmarks BLOB NOT NULL)
        ''')
        conn.commit()
        conn.close()

    def get_next_id(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT MAX(id) FROM faces")
        result = c.fetchone()[0]
        conn.close()
        
        if result is None:
            return "00000"
        
        current_num = int(result)
        next_num = current_num + 1
        return f"{next_num:05d}"

    def load_references_from_db(self):
        references = {}
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, name, landmarks FROM faces")
        rows = c.fetchall()
        conn.close()
        
        for row in rows:
            id_num, name, landmarks_blob = row
            landmarks = pickle.loads(landmarks_blob)
            references[name] = {
                'landmarks': landmarks,
                'id': id_num
            }
        return references

    def save_to_database(self, name, landmarks):
        id_num = self.get_next_id()
        landmarks_blob = pickle.dumps(landmarks)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO faces (id, name, landmarks) VALUES (?, ?, ?)",
                      (id_num, name, landmarks_blob))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao salvar no banco de dados: {e}")
            return False
        finally:
            conn.close()

    def start_registration(self):
        name = self.register_name.get().strip()
        if not name:
            messagebox.showerror("Erro", "Por favor, insira um nome para cadastro")
            return
        name = name.upper()
        self.root.iconify()
        self.capture_image_for_registration(name)

    def capture_image_for_registration(self, name):
        cap = cv2.VideoCapture(0)
        countdown = 5
        start_time = time.time()
        
        with self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5) as face_mesh:
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_time = time.time()
                elapsed_time = int(current_time - start_time)
                remaining_time = max(0, countdown - elapsed_time)
                
                cv2.putText(frame, f"Capturando em: {remaining_time}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Registro - Captura de Imagem', frame)
                
                if remaining_time == 0:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = face_mesh.process(frame_rgb)
                    
                    if results.multi_face_landmarks:
                        landmarks = np.array([[landmark.x, landmark.y] for landmark in results.multi_face_landmarks[0].landmark]).flatten()
                        
                        if self.save_to_database(name, landmarks):
                            messagebox.showinfo("Sucesso", f"Cadastro realizado com sucesso para {name}")
                        else:
                            messagebox.showerror("Erro", "Falha ao salvar no banco de dados")
                        break
                    else:
                        messagebox.showerror("Erro", "Nenhum rosto detectado. Tente novamente.")
                        break
                
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        self.root.deiconify()
        self.show_frame(self.frame_main)
        
        # Recarregar as referências após o novo cadastro
        self.reference_data = self.load_references_from_db()

    def calculate_distance(self, face_landmarks1, face_landmarks2):
        min_length = min(len(face_landmarks1), len(face_landmarks2))
        return np.linalg.norm(face_landmarks1[:min_length] - face_landmarks2[:min_length])

    def start_recognition(self):
        username = self.username.get().strip()
        if not username:
            messagebox.showerror("Erro", "Por favor, insira um nome de usuário")
            return
        
        self.root.iconify()
        self.run_face_recognition(username)

    def run_face_recognition(self, username):
        cap = cv2.VideoCapture(0)
        threshold = 0.7

        with self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6) as face_mesh:
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Falha ao capturar frame")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame_rgb)
                
                access_granted = False
                recognized_name = None

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        landmarks = np.array([[landmark.x, landmark.y] for landmark in face_landmarks.landmark]).flatten()
        
                        min_distance = float('inf')
                        recognized_id = None
                        recognized_name = None
        
                        for name, ref_data in self.reference_data.items():
                            distance = self.calculate_distance(landmarks, ref_data['landmarks'])
                            if distance < min_distance:
                                    min_distance = distance
                                    if distance < threshold:
                                        recognized_name = name
                                        recognized_id = ref_data['id']

                        self.mp_drawing.draw_landmarks(
                        frame, face_landmarks, self.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1))
        
                        if recognized_name:
                            if recognized_name.lower() == username.lower():
                                message = f"ACESSO LIBERADO {recognized_name}. SEU ID: {recognized_id}"  # Mostrando ID e nome
                                color = (0, 255, 0)
                                access_granted = True
                            else:
                                message = f"ACESSO NEGADO {recognized_name}. SEU ID: {recognized_id}"  # Mostrando ID e nome
                                color = (0, 0, 255)
                        else:
                            message = "Pessoa nao reconhecida"
                            color = (0, 0, 255)
                        
                        cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.50, color, 1)

                cv2.imshow('Reconhecimento Facial', frame)
                
                key = cv2.waitKey(1)
                if key & 0xFF == 27 or (access_granted and key & 0xFF == ord('q')):
                    break

        cap.release()
        cv2.destroyAllWindows()
        self.root.deiconify()
        self.show_frame(self.frame_main)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()