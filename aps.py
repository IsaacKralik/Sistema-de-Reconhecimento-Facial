import tkinter as tk
from tkinter import messagebox
import mediapipe as mp
import os
import sqlite3
import cv2
import time
import numpy as np
from PIL import Image
import io
import face_recognition

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reconhecimento Facial")
        self.root.geometry("400x600")
        
        self.username = tk.StringVar()
        self.frame_main = tk.Frame(root)
        self.frame_login = tk.Frame(root)
        self.frame_register = tk.Frame(root)
        self.frame_teste = tk.Frame(root)
        
        self.setup_main_frame()
        self.setup_login_frame()
        self.setup_register_frame()
        self.setup_teste_frame()
        
        self.mp_face_mesh = mp.solutions.face_mesh

        self.show_frame(self.frame_main)
    
    def setup_main_frame(self):
        tk.Label(self.frame_main, text="Escolha uma opção:").pack(pady=20)
        tk.Button(self.frame_main, text="Login", command=lambda: self.show_frame(self.frame_login)).pack(pady=10)
        tk.Button(self.frame_main, text="Cadastrar", command=lambda: self.show_frame(self.frame_register)).pack()
        tk.Button(self.frame_main, text="teste", command=lambda: self.show_frame(self.frame_teste)).pack()

    def setup_login_frame(self):
        tk.Label(self.frame_login, text="Nome de Usuário:").pack(pady=10)
        tk.Entry(self.frame_login, textvariable=self.username).pack()
        tk.Button(self.frame_login, text="Login", command=self.start_recognition).pack(pady=20)
        tk.Button(self.frame_login, text="Voltar", command=lambda: self.show_frame(self.frame_main)).pack()

    def setup_register_frame(self):
        self.registrar_nome = tk.StringVar()
        self.registrar_sobrenome = tk.StringVar()
        self.registrar_dt_nasc = tk.StringVar()
        self.registrar_genero = tk.StringVar()
        self.registrar_nl_acesso = tk.StringVar()
        self.registrar_cpf = tk.StringVar()
        self.registrar_email = tk.StringVar()
        self.registrar_senha = tk.StringVar()

        tk.Label(self.frame_register, text="Nome:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_nome).pack()
        tk.Label(self.frame_register, text="Sobrenome:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_sobrenome).pack()
        tk.Label(self.frame_register, text="Data de nascimento:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_dt_nasc).pack()
        tk.Label(self.frame_register, text="Gênero:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_genero).pack()
        tk.Label(self.frame_register, text="Nível de acesso:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_nl_acesso).pack()
        tk.Label(self.frame_register, text="CPF:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_cpf).pack()
        tk.Label(self.frame_register, text="E-mail:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_email).pack()
        tk.Label(self.frame_register, text="Senha:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_senha).pack()


        tk.Button(self.frame_register, text="Próximo", command=self.registro).pack(pady=20)
        tk.Button(self.frame_register, text="Voltar", command=lambda: self.show_frame(self.frame_main)).pack()

    def setup_teste_frame(self):
        tk.Button(self.frame_teste, text="Teste", command=self.start_update).pack(pady=20)
        tk.Button(self.frame_teste, text="Teste img", command=self.capturar_foto).pack(pady=20)
        tk.Button(self.frame_teste, text="Teste comparacao", command=self.comparacao).pack(pady=20)
        tk.Button(self.frame_teste, text="Voltar", command=lambda: self.show_frame(self.frame_main)).pack()

    def show_frame(self, frame):
        self.frame_main.pack_forget()
        self.frame_login.pack_forget()
        self.frame_register.pack_forget()
        self.frame_teste.pack_forget()
        frame.pack()
    
    def start_recognition(self):
        print('reconhecimento')

    def registro(self):
        nome = self.registrar_nome.get().strip()
        sobrenome = self.registrar_sobrenome.get().strip()
        dt_nasc = self.registrar_dt_nasc.get().strip()
        genero = self.registrar_genero.get().strip()
        nl_acesso = self.registrar_nl_acesso.get().strip()
        cpf = self.registrar_cpf.get().strip()
        email = self.registrar_email.get().strip()
        senha = self.registrar_senha.get().strip()

        if nome and sobrenome and dt_nasc and genero and nl_acesso and cpf and email and senha:
            if(not self.usuario_existe(cpf)):
                foto = self.capturar_foto()
                status = self.enviar_bd(nome, sobrenome, dt_nasc, genero, nl_acesso, cpf, email, senha, foto)

                if status:
                    messagebox.showerror("Sucesso", "Usuário inserido com sucesso!")
            else:
                messagebox.showerror("Erro", "Usuário já existe!")
        else:
            print('nulo')
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return

    def start_update(self):
        conn = sqlite3.connect("bd.db")
        cursor = conn.execute("SELECT * FROM user")
        for row in cursor:
            print(row)
        conn.commit()
        conn.close()

    def capturar_foto(self):
        cap = cv2.VideoCapture(0)
        contagem = 5
        tempo_inicial = time.time()

        with self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5) as face_mesh:
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                tempo_atual = time.time()
                tempo_gasto = int(tempo_atual - tempo_inicial)
                tempo_faltante = max(0, contagem - tempo_gasto)
                
                cv2.putText(frame, f"Capturando em: {tempo_faltante}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Registro - Captura de Imagem', frame)
                
                if tempo_faltante == 0:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = face_mesh.process(frame_rgb)
                    
                    if results.multi_face_landmarks:
                        img = Image.fromarray(frame_rgb)
                        foto = io.BytesIO()
                        img.save(foto, format="PNG")
                        foto = foto.getvalue()

                        #self.enviar_bd(nome, sobrenome, dt_nasc, genero, nl_acesso, cpf, email, senha, foto)
                        return foto
                        #conn = sqlite3.connect("bd.db")
                        #conn.execute("INSERT INTO photos (id, photo) VALUES (?, ?)", (1, foto))
                        #conn.commit()
                        #conn.close()
                        break
                    else:
                        print('não foi')
                        break
                
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        self.root.deiconify()
        self.show_frame(self.frame_main)

    def usuario_existe(self, cpf):
        conn = sqlite3.connect("bd.db")
        with conn:
            busca_usuario = conn.execute(f"SELECT count(*) FROM user WHERE cpf = '{cpf}'")
            usuario = busca_usuario.fetchone()[0]
        
        conn.close()

        if usuario == 0:
            return False
        else:
            return True

    def enviar_bd(self, nome, sobrenome, dt_nasc, genero, nl_acesso, cpf, email, senha, foto):
        conn = sqlite3.connect("bd.db")
        conn.execute("INSERT INTO user (nome, sobrenome, data_nasc, genero, nivel_acesso, cpf, email, senha) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nome, sobrenome, dt_nasc, genero, nl_acesso, cpf, email, senha))
        conn.commit()

        with conn:
            id_consulta = conn.execute(f"SELECT id FROM user WHERE cpf = '{cpf}'")
            id_usuario = id_consulta.fetchone()[0]
        print(id_usuario)
        conn.execute("INSERT INTO photos (id_user, photo) VALUES (?, ?)", (id_usuario, foto))
        conn.commit()
        conn.close()

        return True

    def comparacao(self):
        conn = sqlite3.connect("bd.db")
        cursor = conn.execute("SELECT photo FROM photos where id_user = 1")
        result = cursor.fetchone()
        conn.close()

        if result:
            image_data = result[0]
            image = Image.open(io.BytesIO(image_data))
            img = np.array(image)

        img_bd = face_recognition.face_encodings(img)
        img_bd = img_bd[0]

        cap = cv2.VideoCapture(0)
        contagem = 5
        tempo_inicial = time.time()

        with self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5) as face_mesh:
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                tempo_atual = time.time()
                tempo_gasto = int(tempo_atual - tempo_inicial)
                tempo_faltante = max(0, contagem - tempo_gasto)
                
                cv2.putText(frame, f"Capturando em: {tempo_faltante}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Registro - Captura de Imagem', frame)
                
                if tempo_faltante == 0:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = face_mesh.process(frame_rgb)
                    
                    if results.multi_face_landmarks:
                        frame = frame_rgb
                        break
                    else:
                        print('não foi')
                        break
                
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        self.root.deiconify()
        
        img_nova = face_recognition.face_encodings(frame)

        img_nova = img_nova[0]

        # Compara a imagem capturada com a imagem do banco
        results = face_recognition.compare_faces([img_bd], img_nova)
        print(results[0])
        return results[0]


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()