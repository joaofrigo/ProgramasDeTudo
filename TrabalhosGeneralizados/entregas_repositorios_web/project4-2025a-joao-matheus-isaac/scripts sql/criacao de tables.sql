CREATE TABLE IF NOT EXISTS lutador (
  id_lutador SERIAL PRIMARY KEY,
  nome VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS golpe (
  id_golpe SERIAL PRIMARY KEY,
  id_lutador INT,
  FOREIGN KEY (id_lutador) REFERENCES lutador(id_lutador),
  nome VARCHAR(255),
  tipo VARCHAR(30), -- Qual membro do corpo usa o golpe, cabeça, braços, pernas ou especial.
  descricao VARCHAR(255),
  forca VARCHAR(30) -- Se é leve, médio ou forte (velocidade basicamente)
);

CREATE TABLE IF NOT EXISTS amizades (
  id_lutador INT,
  id_amigo INT,
  FOREIGN KEY (id_lutador) REFERENCES lutador(id_lutador),
  FOREIGN KEY (id_amigo) REFERENCES lutador(id_lutador),
  PRIMARY KEY (id_lutador, id_amigo)
);

CREATE TABLE IF NOT EXISTS inimizades (
  id_lutador INT,
  id_inimigo INT,
  FOREIGN KEY (id_lutador) REFERENCES lutador(id_lutador),
  FOREIGN KEY (id_inimigo) REFERENCES lutador(id_lutador),
  PRIMARY KEY (id_lutador, id_inimigo)
);
