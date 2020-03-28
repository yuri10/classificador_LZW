# classificador_LZW

O objetivo deste projeto é implementar um reconhecedor de padrões baseado no LZW. O objetivo específico é classificar diversas imagens de faces em suas verdadeiras categorias. Utilizou-se um banco de dados previamente rotulado, ORL Database of Faces, contando com 40 pessoas e cada pessoa possuindo 10 imagens da face. Destas 10 imagens de cada pessoa, 9 serão separadas para contrução e treinamento de um dicionário utilizando o algoritmo LZW. Este processo de treinamento é feito para as 40 pessoas do banco de dados. O processo de teste utiliza a imagem que sobrou de cada pessoa e passa pela compressão de todos os dicionários gerados pelas 40 pessoas, o dicionário (da pessoa) que comprimir melhor a imagem de teste será considerado a classificação mais correta.  

A base de dados de face pode ser encontrada no link abaixo  
https://www.dropbox.com/s/mnhfhb1i51loknk/orl_faces.zip?dl=0  


