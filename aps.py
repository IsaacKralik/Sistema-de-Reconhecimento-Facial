# Importação de bibliotecas
import tkinter as tk
from tkinter import messagebox
import mediapipe as mp
import sqlite3
import cv2
import time
import numpy as np
from PIL import Image
import io
import face_recognition

# Criação da classe principal do programa
class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root # Definição da raíz utilizada pelos componentes da biblioteca visual tkinter
        self.root.title("Sistema de Reconhecimento Facial") # Título da janela do programa
        self.root.geometry("400x600") # Tamanho da janela do programa
        self.senha = False # Variável usada para armazenar temporariamente a senha do usuário para autenticação

        # Definição dos frames utilizados em cada página do programa
        self.frame_main = tk.Frame(root)
        self.frame_login = tk.Frame(root)
        self.frame_register = tk.Frame(root)
        self.frame_sucesso1 = tk.Frame(root)
        self.frame_sucesso2 = tk.Frame(root)
        self.frame_sucesso3 = tk.Frame(root)
        self.frame_login_nivel3 = tk.Frame(root)
        
        # Definição das funções que constroem os frames
        self.setup_main_frame()
        self.setup_register_frame()
        self.setup_sucesso1_frame()
        self.setup_sucesso2_frame()
        self.setup_sucesso3_frame()
        self.setup_login_nivel3_frame()
        
        self.mp_face_mesh = mp.solutions.face_mesh

        # Parametrização da função que troca os frames, definindo a página inicial como primeira ao executar o programa
        self.mostrar_frame(self.frame_main)
    
    # Construção da página incial
    def setup_main_frame(self):
        tk.Label(self.frame_main, text="Escolha uma opção:").pack(pady=20)
        tk.Button(self.frame_main, text="Login", command=self.start_recognition).pack(pady=20)
        tk.Button(self.frame_main, text="Cadastrar", command=lambda: self.mostrar_frame(self.frame_register)).pack()

    # Construção da página de registro de usuário
    def setup_register_frame(self):
        opcoes = [
            "1",
            "2",
            "3"
        ]

        self.registrar_nome = tk.StringVar()
        self.registrar_sobrenome = tk.StringVar()
        self.registrar_dt_nasc = tk.StringVar()
        self.registrar_genero = tk.StringVar()
        self.registrar_nl_acesso = tk.StringVar()
        self.registrar_nl_acesso.set("1")
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
        tk.OptionMenu( self.frame_register , self.registrar_nl_acesso , *opcoes ).pack()
        tk.Label(self.frame_register, text="CPF:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_cpf).pack()
        tk.Label(self.frame_register, text="E-mail:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_email).pack()
        tk.Label(self.frame_register, text="Senha:").pack(pady=10)
        tk.Entry(self.frame_register, textvariable=self.registrar_senha, show="*", width=15).pack()

        tk.Button(self.frame_register, text="Próximo", command=self.registro).pack(pady=20)
        tk.Button(self.frame_register, text="Voltar", command=lambda: self.mostrar_frame(self.frame_main)).pack()

    # Construção da página de sucesso para usuários de nível 1
    def setup_sucesso1_frame(self):
        tk.Label(self.frame_sucesso1, text="Sucesso!").pack(pady=10)
        tk.Label(self.frame_sucesso1, text="Confira os conteúdos disponíveis para o nível de acesso 1!").pack(pady=10)

    # Construção da página de sucesso para usuários de nível 2
    def setup_sucesso2_frame(self):
        tk.Label(self.frame_sucesso2, text="Sucesso!").pack(pady=10)
        tk.Label(self.frame_sucesso2, text="Confira os conteúdos disponíveis para o nível de acesso 2!").pack(pady=10)
    
    # Construção da página de sucesso para usuários de nível 3
    def setup_sucesso3_frame(self):
        tk.Label(self.frame_sucesso3, text="Sucesso!").pack(pady=10)
        tk.Label(self.frame_sucesso3, text="Confira os conteúdos disponíveis para o nível de acesso 3!").pack(pady=10)

    # Construção da página de dupla autenticação para usuários do nível 3
    def setup_login_nivel3_frame(self):
        self.senha_proposta = tk.StringVar()

        tk.Label(self.frame_login_nivel3, text="Como verificação de segurança, insira sua senha:").pack(pady=10)
        tk.Entry(self.frame_login_nivel3, textvariable=self.senha_proposta, show="*", width=15).pack()

        tk.Button(self.frame_login_nivel3, text="Próximo", command=self.verificar_acesso3).pack(pady=20)

    # Função que executa a troca de frames do programa
    # Desabilita todos os frames e habilita apenas o frame recebido por parâmetro
    def mostrar_frame(self, frame):
        self.frame_main.pack_forget()
        self.frame_login.pack_forget()
        self.frame_register.pack_forget()
        self.frame_sucesso1.pack_forget()
        self.frame_sucesso2.pack_forget()
        self.frame_sucesso3.pack_forget()
        self.frame_login_nivel3.pack_forget()
        frame.pack()
    
    # Função que atua quando o usuário envia o formulário de registro
    def registro(self):
        # Variáveis com os valores de cada campo disponível
        nome = self.registrar_nome.get().strip()
        sobrenome = self.registrar_sobrenome.get().strip()
        dt_nasc = self.registrar_dt_nasc.get().strip()
        genero = self.registrar_genero.get().strip()
        nl_acesso = self.registrar_nl_acesso.get().strip()
        cpf = self.registrar_cpf.get().strip()
        email = self.registrar_email.get().strip()
        senha = self.registrar_senha.get().strip()

        # Verifica se todos os campos estão preenchidos.
        ## Caso sim, chama a função de captura de foto para o cadastro, e em seguida a função que envia todos os dados para o banco de dados
        ## Caso negativo, exibe uma mensagem de erro e libera o formulário para o usuário preencher o que falta.
        if nome and sobrenome and dt_nasc and genero and nl_acesso and cpf and email and senha:
            if(not self.usuario_existe(cpf)):
                foto = self.capturar_foto()
                status = self.enviar_bd(nome, sobrenome, dt_nasc, genero, nl_acesso, cpf, email, senha, foto)

                if status:
                    messagebox.showerror("Sucesso", "Usuário inserido com sucesso!")
            else:
                messagebox.showerror("Erro", "Usuário já existe!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return

    # Função usada para capturar uma foto do usuário, usada para cadastro
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
                        return foto
                        break
                    else:
                        break
                
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        self.root.deiconify()
        self.mostrar_frame(self.frame_main)

    def start_recognition(self):
        usuario = self.comparacao()
        conn = sqlite3.connect("bd.db")

        with conn:
            try:
                busca_senha = conn.execute(f"SELECT senha FROM user WHERE id = {usuario[0]}")
                self.senha = busca_senha.fetchone()[0]
            except:
                messagebox.showerror("Erro", "Nenhum usuário cadastrado. Efetue um cadastro e tente novamente!")
                self.mostrar_frame(self.frame_main)
                return 0

        with conn:
            busca_usuario = conn.execute(f"SELECT nivel_acesso FROM user WHERE id = {usuario[0]}")
            nivel = busca_usuario.fetchone()[0]
        
        match nivel:
            case 1:
                self.mostrar_frame(self.frame_sucesso1)
                pass
            case 2:
                self.mostrar_frame(self.frame_sucesso2)
            case 3:
                self.mostrar_frame(self.frame_login_nivel3)
            case _:
                messagebox.showerror("Erro", "Nível de acesso inconsistente. Entre em contato com a administração para resolver o problema.")
                self.mostrar_frame(self.frame_main)

        conn.close()

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
        conn.execute("INSERT INTO photos (id_user, photo) VALUES (?, ?)", (id_usuario, foto))
        conn.commit()
        conn.close()

        return True

    def comparacao(self):
        conn = sqlite3.connect("bd.db")
        cursor = conn.execute("SELECT id_user, photo FROM photos")

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
                        break
                
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        self.root.deiconify()
        
        img_nova = face_recognition.face_encodings(frame)

        img_nova = img_nova[0]

        # Compara a imagem capturada com a imagem do banco
        for row in cursor:
            image_data = row[1]
            image = Image.open(io.BytesIO(image_data))
            img = np.array(image)


            img_bd = face_recognition.face_encodings(img)
            img_bd = img_bd[0]
            results = face_recognition.compare_faces([img_bd], img_nova)
            if(results[0]):
                return [row[0]]
        conn.close()

    def verificar_acesso3(self):
        senha = self.senha
        senha_prop = self.senha_proposta.get().strip()
        
        if senha == False:
            return 0
        else:
            if (senha != False) and (senha_prop == senha):
                self.mostrar_frame(self.frame_sucesso3)
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
                self.mostrar_frame(self.frame_main)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()