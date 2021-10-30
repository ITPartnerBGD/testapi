from flask import Flask, request, jsonify
import json
import sqlite3


app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('bookings.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn


@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM bookings ORDER BY pravnolice")
        bookings = [
            dict(id=row[0] , pravnolice=row[1], fizickolice=row[2], tiplicence=row[3], pcname=row[4], serijskibrojpc=row[5], guid=row[6], vazidogodine=row[7], pclogin=row[8], blokirano=row[9], problematicno=row[10], poslednjipristup=row[11])
            for row in cursor.fetchall()
        ]
        if bookings is not None:
            return jsonify(bookings)

    if request.method == 'POST':
        new_pravnolice      = request.form['pravnolice'] 
        new_fizickolice     = request.form['fizickolice']
        new_tiplicence      = request.form['tiplicence']
        new_pcname          = request.form['pcname']
        new_serijskibrojpc  = request.form['serijskibrojpc']
        new_guid            = request.form['guid']
        new_vazidogodine    = request.form['vazidogodine']
        new_pclogin         = request.form['pclogin']
        new_blokirano       = request.form['blokirano']
        new_problematicno   = request.form['problematicno']
        new_poslednjipristup= request.form['poslednjipristup']

        sql = """INSERT INTO bookings (pravnolice, fizickolice, tiplicence, pcname, serijskibrojpc, guid, vazidogodine, pclogin, blokirano, problematicno, poslednjipristup )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"""
        cursor = cursor.execute(sql, (new_pravnolice, new_fizickolice, new_tiplicence, new_pcname, new_serijskibrojpc, new_guid, new_vazidogodine, new_pclogin, new_blokirano, new_problematicno, new_poslednjipristup ))
        conn.commit()
        return f"Booking with the id: {cursor.lastrowid} created successful", 201


@app.route('/bookings/<guid>', methods=['GET', 'PUT', 'DELETE'])
def single_booking(guid):
    conn = db_connection()
    cursor = conn.cursor()
    booking = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM bookings WHERE guid=?", (guid,))
        rows = cursor.fetchall()
        for r in rows:
            booking = r
        if booking is not None:
            return jsonify(booking), 200
        else:
            return "Something wrong", 404

    if request.method == 'PUT':
        sql = """UPDATE bookings
                SET pravnolice=?,
                    fizickolice=?,
                    tiplicence=?,
                    pcname=?,
                    serijskibrojpc=?,
                    guid=?,
                    vazidogodine=?,
                    pclogin=?,
                    blokirano=?,
                    problematicno=?,
                    poslednjipristup=?
                WHERE guid=? """
        pravnolice      = request.form["pravnolice"]
        fizickolice     = request.form["fizickolice"]
        tiplicence      = request.form["tiplicence"]
        pcname          = request.form["pcname"]
        serijskibrojpc  = request.form["serijskibrojpc"]
        guid            = request.form["guid"]
        vazidogodine    = request.form["vazidogodine"]
        pclogin         = request.form["pclogin"]
        blokirano       = request.form["blokirano"]
        problematicno   = request.form["problematicno"]
        poslednjipristup= request.form["poslednjipristup"]
        updated_bookings = {
            "pravnolice": pravnolice,
            "fizickolice": fizickolice,
            "tiplicence": tiplicence,
            "pcname": pcname,
            "serijskibrojpc": serijskibrojpc,
            "guid": guid,
            "vazidogodine": vazidogodine,
            "pclogin": pclogin,
            "blokirano": blokirano,
            "problematicno": problematicno,
            "poslednjipristup": poslednjipristup,
        }
        conn.execute(sql, (pravnolice, fizickolice, tiplicence, pcname, serijskibrojpc, guid, vazidogodine, pclogin, blokirano, problematicno, poslednjipristup, guid))
        conn.commit()
        return jsonify(updated_bookings)

    if request.method == 'DELETE':
        sql = """ DELETE FROM bookings WHERE guid=? """
        conn.execute(sql, (guid,))
        conn.commit()
        return "The booking with id: {} has been deleted.".format(guid), 200


if __name__ == '__main__':
   app.run()