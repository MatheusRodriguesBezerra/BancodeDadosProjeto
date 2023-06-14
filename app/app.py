import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

@APP.route('/')
def index():
    stats = {}
    x = db.execute('SELECT COUNT(*) AS cantores FROM CANTOR').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS bandas FROM BANDA').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS musicas FROM MUSICA').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS palcos FROM PALCO').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS espetaculos FROM ESPETACULO').fetchone()
    stats.update(x)

    logging.info(stats)
    return render_template('index.html',stats=stats)

@APP.route('/bandas/')
def list_bandas():
    bandas = db.execute(
      '''
      SELECT BandaId, Nome, Nacionalidade, NdeIntegrantes 
      FROM BANDA
      ORDER BY Nome
      ''').fetchall()
    return render_template('banda-list.html', bandas=bandas)


@APP.route('/bandas/<int:id>/')
def get_banda(id):
  banda = db.execute(
      '''
      SELECT BandaId, Nome, Nacionalidade, NdeIntegrantes 
      FROM BANDA 
      WHERE bandaId = %s
      ''', id).fetchone()

  if banda is None:
     abort(404, 'Banda id {} não existe.'.format(id))
    
  cantores = db.execute('''
    SELECT c.Nome AS cNome,
    c.CantId AS cCantId
    FROM CANTOR c
    JOIN CANTOR_BANDA cb
    JOIN BANDA b
    ON c.CantId = cb.CantId AND cb.bandaId = b.bandaId
    WHERE b.bandaId = %s
    ''',id).fetchall()

  return render_template('banda.html', banda=banda, cantores=cantores)

@APP.route('/bandas/search/<expr>/')
def search_banda(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  bandas = db.execute(
      ''' 
      SELECT BandaId, Nome, Nacionalidade, NdeIntegrantes
      FROM BANDA 
      WHERE Nome LIKE %s
      ''', expr).fetchall()
  return render_template('banda-search.html',
           search=search,bandas=bandas)

# Actors
@APP.route('/cantores/')
def list_actors():
    cantores = db.execute('''
      SELECT CantId,Nome,Nacionalidade 
      FROM CANTOR
      ORDER BY Nome
    ''').fetchall()
    return render_template('cantor-list.html', cantores=cantores)


@APP.route('/cantores/<int:id>/')
def view_movies_by_actor(id):
  cantor = db.execute(
    '''
    SELECT CantId, Nome, Nacionalidade
    FROM CANTOR 
    WHERE CantId = %s
    ''', id).fetchone()

  musicas = db.execute('''
    SELECT c.Nome AS cNome,
	  m.Nome AS mNome,
    m.MusicaId AS mMusicaId 
    FROM CANTOR c
    JOIN ESPETACULO_CANTOR ec
	  JOIN ESPETACULO e
    JOIN ESPETACULO_MUSICA em
    JOIN MUSICA m
    ON c.CantId = ec.CantId AND ec.EspetaculoId = e.EspetaculoId AND e.EspetaculoId = em.EspetaculoId AND em.MusicaId = m.MusicaId
    WHERE c.CantId = %s
    ''',id).fetchall()

  espetaculo = db.execute(
    '''
    SELECT e.EspetaculoId AS eEspetaculoId
    FROM ESPETACULO e
    JOIN ESPETACULO_CANTOR ec
    JOIN CANTOR c
    ON e.EspetaculoId = ec.EspetaculoId AND ec.CantId = c.CantId
    WHERE c.CantId = %s
    LIMIT 1
    ''', id).fetchone()

  if cantor is None:
     abort(404, 'Cantor id {} não existe.'.format(id))

  return render_template('cantor.html', cantor=cantor, musicas=musicas, espetaculo=espetaculo)
 
@APP.route('/cantores/search/<expr>/')
def search_cantor(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  cantores = db.execute(
      ''' 
      SELECT CantId, Nome, Nacionalidade
      FROM CANTOR 
      WHERE Nome LIKE %s
      ''', expr).fetchall()

  return render_template('cantor-search.html', 
           search=search,cantores=cantores)

@APP.route('/musicas/')
def list_musicas():
    musicas = db.execute('''
      SELECT MusicaId, Nome 
      FROM MUSICA
      ORDER BY Nome
    ''').fetchall()
    return render_template('musica-list.html', musicas=musicas)

@APP.route('/musicas/<int:id>/')
def view_movies_by_genre(id):
  musica = db.execute(
    '''
    SELECT MusicaId, Nome
    FROM MUSICA 
    WHERE MusicaId = %s
    ''', id).fetchone()

  if musica is None:
     abort(404, 'Musica id {} não existe.'.format(id))

  espetaculo = db.execute(
    '''
    SELECT e.EspetaculoId AS eEspetaculoId
    FROM MUSICA m
    JOIN ESPETACULO_MUSICA em
    JOIN ESPETACULO e
    ON m.MusicaId = em.MusicaId AND em.EspetaculoId = e.EspetaculoId
    WHERE m.musicaId = %s
    ''', id).fetchone()

  cantores = db.execute('''
      SELECT c.Nome AS cNome,
      c.CantId AS cCantId
      FROM CANTOR c
      JOIN ESPETACULO_CANTOR ec
      JOIN ESPETACULO e
      JOIN ESPETACULO_MUSICA em
      JOIN MUSICA m
      ON c.CantId = ec.CantId AND ec.EspetaculoId = e.EspetaculoId AND e.EspetaculoId = em.EspetaculoId AND em.MusicaId = m.MusicaId 
      WHERE m.MusicaId = %s
    ''', id).fetchall()

  return render_template('musica.html', musica=musica, cantores=cantores, espetaculo=espetaculo) 

@APP.route('/palcos/')
def list_palcos():
    palcos = db.execute('''
      SELECT PalcoId, Nome 
      FROM PALCO
      ORDER BY Nome
    ''').fetchall()
    return render_template('palco-list.html', palcos=palcos)

@APP.route('/palcos/<int:id>/')
def view_palco(id):
  palco = db.execute(
    '''
    SELECT PalcoId, Nome
    FROM PALCO 
    WHERE PalcoId = %s
    ''', id).fetchone()

  cantores = db.execute('''
      SELECT c.Nome AS cNome,
      c.CantId AS cCantId
      FROM CANTOR c
      JOIN ESPETACULO_CANTOR ec
      JOIN ESPETACULO e
      JOIN PALCO p
      ON C.CantId = ec.CantId AND ec.EspetaculoId = e.EspetaculoId AND e.Palco = p.PalcoId
      where p.palcoid = %s
      order by c.Nome
    ''',id).fetchall()

  if palco is None:
     abort(404, 'Palco id {} não existe.'.format(id))
  
  return render_template('palco.html', palco=palco, cantores=cantores)

@APP.route('/espetaculos/')
def list_espetaculos():
    espetaculos = db.execute('''
      SELECT e.EspetaculoId AS eEspetaculoId, 
      p.Nome AS pNome,
      p.PalcoId AS pPalcoId, 
      e.Data AS eData
      FROM ESPETACULO e
      JOIN PALCO p
      ON p.PalcoId = e.Palco
      ORDER BY Data
    ''').fetchall()
    return render_template('espetaculo-list.html', espetaculos=espetaculos)

@APP.route('/espetaculos/<int:id>/')
def view_espetaculo(id):
  espetaculo = db.execute(
    '''
    SELECT e.EspetaculoId AS eEspetaculoId, 
    p.Nome AS pNome,
    e.Data AS eData
    FROM ESPETACULO e
    JOIN PALCO p
    ON p.PalcoId = e.Palco
    WHERE EspetaculoId = %s
    ''', id).fetchone()

  cantores = db.execute(
    '''
    SELECT c.Nome AS cNome,
	  c.CantId AS cCantId,
    c.Nacionalidade AS cNacionalidade,
	  e.EspetaculoId AS eEspetaculoId
    FROM CANTOR c
    JOIN ESPETACULO_CANTOR ec
	  JOIN ESPETACULO e
    ON c.CantId = ec.CantId AND ec.EspetaculoId = e.EspetaculoId
    WHERE e.EspetaculoId = %s
    ''', id).fetchall()

  musicas = db.execute(
    '''
    SELECT m.Nome AS mNome,
	  e.EspetaculoId AS eEspetaculoId,
    m.MusicaId AS mMusicaId
    FROM MUSICA m
    JOIN ESPETACULO_MUSICA em
	  JOIN ESPETACULO e
    ON m.MusicaId = em.MusicaId AND em.EspetaculoId = e.EspetaculoId
    WHERE e.EspetaculoId = %s
    ''', id).fetchall()

  if espetaculo is None:
     abort(404, 'Espetaculo id {} não existe.'.format(id))
  
  return render_template('espetaculo.html', espetaculo=espetaculo, cantores=cantores, musicas=musicas) #movies=movies


