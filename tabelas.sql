use guest;

GRANT ALL PRIVILEGES ON * . * TO 'matheus'@'localhost';

FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS CANTOR (
  CantId int(11) NOT NULL,
  Nome varchar(255) NOT NULL,
  Nacionalidade varchar(255) NOT NULL,
  PRIMARY KEY (CantId)
);

CREATE TABLE IF NOT EXISTS BANDA (
  BandaId int(11) NOT NULL,
  Nome varchar(255) NOT NULL,
  Nacionalidade varchar(255) NOT NULL,
  NdeIntegrantes smallint(6) NOT NULL,
  PRIMARY KEY (BandaId)
);


CREATE TABLE IF NOT EXISTS MUSICA (
  MusicaId int(11) NOT NULL,
  Nome varchar(255) NOT NULL,
  PRIMARY KEY (MusicaId)
);

CREATE TABLE IF NOT EXISTS PALCO (
  PalcoId int(11) NOT NULL,
  Nome varchar(255) NOT NULL,
  PRIMARY KEY (PalcoId)
);

CREATE TABLE IF NOT EXISTS ESPETACULO (
  EspetaculoId int(11) NOT NULL,
  Palco int(11) NOT NULL,
  Data date NOT NULL,
  PRIMARY KEY (EspetaculoId),
  FOREIGN KEY(Palco) REFERENCES PALCO(PalcoId)
);

CREATE TABLE IF NOT EXISTS CANTOR_BANDA (
  BandaId int(11) NOT NULL,
  CantId int(11) NOT NULL,
  PRIMARY KEY (CantId,BandaId),
  FOREIGN KEY(CantId) REFERENCES CANTOR(CantId),
  FOREIGN KEY(BandaId) REFERENCES BANDA(BandaId)
);

CREATE TABLE IF NOT EXISTS ESPETACULO_CANTOR (
  EspetaculoId int(11) NOT NULL,
  CantId int(11) NOT NULL,
  PRIMARY KEY (EspetaculoId,CantId),
  FOREIGN KEY(CantId) REFERENCES CANTOR(CantId),
  FOREIGN KEY(EspetaculoId) REFERENCES ESPETACULO(EspetaculoId)
);

CREATE TABLE  IF NOT EXISTS ESPETACULO_MUSICA (
  EspetaculoId int(11) NOT NULL,
  MusicaId int(11) NOT NULL,
  PRIMARY KEY (EspetaculoId,MusicaId),
  FOREIGN KEY(MusicaId) REFERENCES MUSICA(MusicaId),
  FOREIGN KEY(EspetaculoId) REFERENCES ESPETACULO(EspetaculoId)
);