# SIRELA – Sistema de Identificação e Reconhecimento Facial para Liberação de Acesso

SIRELA é um projeto de autenticação com reconhecimento facial desenvolvido como parte da Atividade Prática Supervisionada do sexto semestre, do curso Ciência da Computação.

O objetivo é limitar o acesso a diferentes partes de um sistema usando o reconhecimento facial, possibilitando que o usuário visualize apenas o que está destinado ao seu nível de acesso.

## Tecnologias usadas
* Python
* IDE VSCODE
* SQLite

## Bibliotecas utilizadas

Para completo funcionamento do código, instale as bibliotecas por meio do arquivo requirements.txt, conforme abaixo
```bash
pip install -r requirements.txt
```

Algumas das principais bibliotecas utilizadas são:
* pandas
* numpy
* tk
* mediapipe
* sqlite3
* cv2
* face_recognition

Obs.: É possível que você enfrete erros ao instalar o face_recognition pelos métodos tradicionais, enfrentando erros com a biblioteca dlib. Para esse projeto, foi instalado o pacote separadamente conforme ordem abaixo ([tutorial original](https://youtu.be/pO150OCX-ac?si=_Uxh_ToTW0D0Adc3)):
* Intalar o arquivo dlib disponível no ([Github](https://github.com/Cfuhfsgh/Dlib-library-Installation)) que atenda sua versão. Para esse tutorial, foi usado a verão abaixo:
```bash
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
```
* Pode ser que seja necessário fazer um downgrade no numpy. Em caso de impedimento, retorna a versão e tente a instalação novamente.

## Uso
Para uso do projeto, recomendamos abrir o VSCode, certificar-se que todas as bibliotecas estão instaladas e executar o código.

Outras alternativas de execução do arquivo podem funcionar, mas não garantimos o mesmo resultado.

## Colaboradores
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/ToxicOtter">
        <img src="https://avatars.githubusercontent.com/u/58179485?v=4" width="100px;" alt="Foto de Toxic Otter no GitHub"/><br>
        <sub>
          <b>Luan Lima Lopes</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/IsaacKralik">
        <img src="https://avatars.githubusercontent.com/u/104790651?v=4" width="100px;" alt="Foto de Isaac Kralik no GitHub"/><br>
        <sub>
          <b>Isaac Kralik</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/Pontuego">
        <img src="https://avatars.githubusercontent.com/u/132208368?v=4" width="100px;" alt="Foto de João Augusto no GitHub"/><br>
        <sub>
          <b>João Augusto</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
