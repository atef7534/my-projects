from flask import Flask, render_template, request, jsonify
import sqlite3

# connection
def connect():
  database = sqlite3.connect(f"data.db")
  return database

# end connection
def close(connection):
  connection.close()

# application
app = Flask(__name__)
name = __name__

# default
@app.route("/")
def index():
  # operations on database
  connection = connect()
  cursor = connection.cursor()
  cursor.execute("DELETE FROM mf WHERE id NOT IN ( SELECT id FROM mf GROUP BY word)")
  rows = cursor.execute("SELECT * FROM mf;").fetchall()
  m_len, f_len = 0, 0
  for row in rows:
    m_len += not row[2]
    f_len += row[2]
  connection.commit()
  close(connection)
  return render_template("index.html", rows=rows, m_len=m_len, f_len=f_len)

# add
@app.route("/add", methods=["POST"])
def add():
  # operations on database
  connection = connect()
  cursor = connection.cursor()

  ROWS = cursor.execute("SELECT * FROM mf").fetchall()
  
  # check id
  id = request.json.get("id")
  word = request.json.get("data")
  myclass = request.json.get("type")

  capital_word = word.capitalize()

  # Check if the record exists and update or insert
  cursor.execute("SELECT * FROM mf WHERE id = ? OR word IN (?, ?)", (id, capital_word, word))
  existing_row = cursor.fetchone()

  if existing_row:
    cursor.execute("UPDATE mf SET word = ? WHERE id = ?", (word, id))
  else:
    cursor.execute("INSERT INTO mf (id, word, type) VALUES (?, ?, ?)", (id, word, myclass))

  connection.commit()
  close(connection)

  return jsonify({"success": True})
  

@app.route("/remove", methods=["POST"])
def remove():
  id = request.json.get("id")
  connection = connect()
  cursor = connection.cursor()
  result = {"success": True}
  try:
    cursor.execute("DELETE FROM mf WHERE id = ?", (id, ))
  except:
    result = {"error": "can't remove row! with specified id..."}
  connection.commit(); close(connection)
  return jsonify(result)

@app.route("/verbs", methods=["GET"])
def verbs():
  connection = connect()
  cursor = connection.cursor()
  rows = cursor.execute("SELECT * FROM verbs GROUP BY verbGM ORDER BY id").fetchall()
  close(connection)
  return render_template("verbs.html", rows=rows)


@app.route("/addverb", methods=["POST"])
def addverb():
    connection = connect()
    cursor = connection.cursor()

    id = request.json.get("id")
    verbGM = request.json.get("verbGM")
    verbAR = request.json.get("verbAR")

    if not verbAR or not verbGM:
      return jsonify({ "success": False, "error": "your inputs are empty!" })

    try:
        cursor.execute("INSERT INTO verbs (id, verbGM, verbAR) VALUES (?, ?, ?)", (id, verbGM, verbAR))
        connection.commit()
    except sqlite3.Error as e:
        return jsonify({ "success": False, "error": str(e) })
    finally:
        connection.close()

    return jsonify({ "success": True })

@app.route("/sentences", methods=["GET"])
def sentences():

  # database connection
  connection = connect()

  # cursor
  cursor = connection.cursor()

  # get all sentences from sentences table & fetch all
  sentences = cursor.execute("SELECT * FROM sentences").fetchall()

  # end connection
  close(connection)

  return render_template("sentences.html", sentences=sentences)

@app.route("/addsentence", methods=["POST"])
def addsentence():
  # database connection
  connection = connect()

  # cursor
  cursor = connection.cursor()

  # get id, senGM, senAR
  id = request.json.get("id")
  senGM = request.json.get("senGM")
  senAR = request.json.get("senAR")

  # query to insert new sentence if the check is true
  if not senGM or not senAR:
    return jsonify({ "success": False, "error":  "there's an empty input ... check it again!"})
  
  try:
    cursor.execute("INSERT INTO sentences (id, sentenceGM, sentenceAR) VALUES (?, ?, ?)", (id, senGM, senAR))

    # commit execution
    connection.commit()

  except sqlite3.Error as e:
    return jsonify({ "success": False, "error": str(e) })

  finally:
    # database end connection
    close(connection)

  return jsonify({ "success": True, "error": "no error" })


@app.route("/editsentence", methods=["POST"])
def editsentence():
  # connection
  connection = connect()

  # cursor
  cursor = connection.cursor()

  id = request.json.get("id")
  content = request.json.get("content")
  type = request.json.get("type")

  if not id or not content or not type:
    return jsonify({ "success": False, "error": "there's an empty fields." })

  if type == "sentenceGM":
    cursor.execute("UPDATE sentences SET sentenceGM = ? WHERE id = ?", (content, id))
  else:
    cursor.execute("UPDATE sentences SET sentenceAR = ? WHERE id = ?", (content, id))

  connection.commit()
  close(connection)

  return jsonify({ "success": True, "error": "no error!..."})
# run application
if name == "__main__":
  app.run(debug=True)