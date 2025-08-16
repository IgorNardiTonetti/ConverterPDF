# ConverterPDF

# Ferramenta PDF Moderna

## Visão Geral
A Ferramenta PDF é uma aplicação versátil projetada para simplificar várias tarefas relacionadas a PDFs. Ela fornece uma interface gráfica amigável construída com `customtkinter`, permitindo que os usuários realizem operações como converter imagens para PDF, mesclar múltiplos PDFs, desbloquear PDFs protegidos, transformar texto em maiúsculas e dividir PDFs em páginas individuais.

## Funcionalidades
- **Converter Imagens para PDF**: Converta facilmente vários formatos de imagem (JPEG, PNG, BMP, etc.) em um único documento PDF.
- **Juntar PDFs**: Combine múltiplos arquivos PDF em um só, mantendo a ordem das páginas.
- **Desbloquear PDFs**: Remova a proteção por senha de arquivos PDF, permitindo o acesso ao seu conteúdo.
- **Transformar Texto em Maiúsculas**: Converta o texto de arquivos ou da entrada do usuário para o formato maiúsculo.
- **Dividir PDFs**: Extraia páginas específicas de um PDF ou salve cada página como um arquivo PDF separado.

## Instalação
Para configurar a Ferramenta PDF, siga estes passos:

1. Clone o repositório:
   ```
   git clone <url-do-repositorio>
   cd modern-pdf-tool
   ```

2. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   ```

## Uso
1. Execute a aplicação:
   ```
   python src/converter.py
   ```

2. Use as abas na GUI para acessar diferentes funcionalidades:
   - **Converter Imagens**: Selecione uma pasta contendo imagens para convertê-las em PDF.
   - **Juntar PDFs**: Adicione arquivos PDF para mesclar e especifique o arquivo de saída.
   - **Desbloquear PDF**: Selecione PDFs criptografados para desbloqueá-los.
   - **Maiúsculas**: Transforme o texto de arquivos ou da entrada do usuário em maiúsculas.
   - **Dividir PDF**: Especifique as páginas a serem extraídas ou extraia todas as páginas em PDFs separados.

## Requisitos
A aplicação requer as seguintes bibliotecas Python:
- `customtkinter`
- `PyPDF2`
- `Pillow`
- `pytesseract` (para funcionalidade de OCR)

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para enviar um pull request ou abrir uma issue para quaisquer melhorias ou correções de bugs.

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
