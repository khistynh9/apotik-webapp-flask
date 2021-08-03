from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
cnx = mysql.connector.connect(
    user='root', password='', host='localhost', database='apotik')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'apotik'


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/masterobat')  # Menampilkan data master obat
def masterobat():
    cur = cnx.cursor()
    cur.execute("SELECT obat.kode_obat, obat.nama_obat, obat.satuan_obat, stok.stok_akhir FROM obat INNER JOIN stok ON obat.kode_obat=stok.kode_obat ORDER BY kode_obat")
    obat = cur.fetchall()
    cur.close()
    return render_template('obat.html', data=obat)


@app.route('/tambahobat', methods=['POST'])  # code untuk simpan data obat
def tambahobat():
    if request.method == 'POST':
        kode_obat = request.form['kode_obat']
        nama_obat = request.form['nama_obat']
        satuan_obat = request.form['satuan']
        stok_awal = 0
        cur = cnx.cursor()
        cur.execute("INSERT INTO obat(kode_obat,nama_obat,satuan_obat) VALUES(%s,%s,%s)",
                    (kode_obat, nama_obat, satuan_obat))
        cur.execute("INSERT INTO stok(kode_obat,stok_akhir) VALUES(%s,%s)",
                    (kode_obat, stok_awal))
        cnx.commit()
        cur.close()
        flash("Data Berhasil Ditambahkan")
        return redirect(url_for('masterobat'))


@app.route('/ubahobat', methods=['POST'])  # code untuk edit data obat
def ubahobat():
    if (request.form['kode_obat']):
        kode_obat = request.form['kode_obat']
        nama_obat = request.form['nama_obat']
        satuan_obat = request.form['satuan']
        cur = cnx.cursor()
        sql = "UPDATE obat SET kode_obat = %s, nama_obat = %s, satuan_obat = %s WHERE kode_obat = %s"
        val = (kode_obat, nama_obat, satuan_obat, kode_obat,)
        cur.execute(sql, val)
        cnx.commit()
        flash("Data Berhasil Diubah")
        return redirect(url_for('masterobat'))


# code untuk hapus data obat
@app.route('/hapusobat/<string:kode_obat>', methods=['GET'])
def hapusobat(kode_obat):
    cur = cnx.cursor()
    cur.execute("DELETE FROM obat WHERE kode_obat=%s", (kode_obat,))
    cnx.commit()
    cur.close()
    flash("Data Berhasil Dihapus")
    return redirect(url_for('masterobat'))


@app.route('/mastersuplier')  # Menampilkan data master suplier
def mastersuplier():
    cur = cnx.cursor()
    cur.execute("SELECT * FROM suplier")
    suplier = cur.fetchall()
    cur.close()
    return render_template('suplier.html', data=suplier)


# code untuk simpan data suplier
@app.route('/tambahsuplier', methods=['POST'])
def tambahsuplier():
    if request.method == 'POST':
        nama = request.form['nama']
        telepon = request.form['telepon']
        alamat = request.form['alamat']
        cur = cnx.cursor()
        cur.execute("INSERT INTO suplier(nama,telepon,alamat) VALUES(%s,%s,%s)",
                    (nama, telepon, alamat))
        cnx.commit()
        cur.close()
        flash("Data Berhasil Ditambahkan")
        return redirect(url_for('mastersuplier'))


@app.route('/ubahsuplier', methods=['POST'])  # code untuk edit data suplier
def ubahsuplier():
    if (request.form['id']):
        my_id = request.form['id']
        nama = request.form['nama']
        telepon = request.form['telepon']
        alamat = request.form['alamat']
        cur = cnx.cursor()
        sql = "UPDATE suplier SET nama = %s, telepon = %s, alamat = %s WHERE id = %s"
        val = (nama, telepon, alamat, my_id,)
        cur.execute(sql, val)
        cnx.commit()
        flash("Data Berhasil Diubah")
        return redirect(url_for('mastersuplier'))


# code untuk hapus data suplier
@app.route('/hapussuplier/<id>', methods=['GET'])
def hapussuplier(id):
    cur = cnx.cursor()
    cur.execute("DELETE FROM suplier WHERE id="+id)
    cnx.commit()
    cur.close()
    flash("Data Berhasil Dihapus")
    return redirect(url_for('mastersuplier'))


@app.route('/masterkonsumen')  # Menampilkan data master konsumen
def masterkonsumen():
    cur = cnx.cursor()
    cur.execute("SELECT * FROM konsumen")
    konsumen = cur.fetchall()
    cur.close()
    return render_template('konsumen.html', data=konsumen)


# code untuk simpan data konsumen
@app.route('/tambahkonsumen', methods=['POST'])
def tambahkonsumen():
    if request.method == 'POST':
        nama = request.form['nama']
        telepon = request.form['no_hp']
        alamat = request.form['alamat']
        cur = cnx.cursor()
        cur.execute("INSERT INTO konsumen(nama,no_hp,alamat) VALUES(%s,%s,%s)",
                    (nama, telepon, alamat))
        cnx.commit()
        cur.close()
        flash("Data Berhasil Ditambahkan")
        return redirect(url_for('masterkonsumen'))


@app.route('/ubahkonsumen', methods=['POST'])  # code untuk edit data konsumen
def ubahkonsumen():
    if (request.form['id']):
        my_id = request.form['id']
        nama = request.form['nama']
        telepon = request.form['no_hp']
        alamat = request.form['alamat']
        cur = cnx.cursor()
        sql = "UPDATE konsumen SET nama = %s, no_hp = %s, alamat = %s WHERE id = %s"
        val = (nama, telepon, alamat, my_id,)
        cur.execute(sql, val)
        cnx.commit()
        flash("Data Berhasil Diubah")
        return redirect(url_for('masterkonsumen'))


# code untuk hapus data konsumen
@app.route('/hapuskonsumen/<id>', methods=['GET'])
def hapuskonsumen(id):
    cur = cnx.cursor()
    cur.execute("DELETE FROM konsumen WHERE id="+id)
    cnx.commit()
    cur.close()
    flash("Data Berhasil Dihapus")
    return redirect(url_for('masterkonsumen'))


@app.route('/pembelian')  # Menampilkan data pembelian
def pembelian():
    cur = cnx.cursor()
    cur.execute("SELECT id,nama FROM suplier")
    suplier = cur.fetchall()
    cur.execute("SELECT kode_obat,nama_obat FROM obat")
    obat = cur.fetchall()
    cur.execute("SELECT * FROM pembelian")
    beli = cur.fetchall()
    date = datetime.now()
    waktu = date.strftime("%Y-%m-%d")
    cur.close()
    return render_template('pembelian.html', sp=suplier, ob=obat, date=waktu, pb=beli)


@app.route('/dataobat', methods=['POST'])  # Menampilkan data obat ajax
def dataobat():
    cur = cnx.cursor()
    cur.execute("SELECT kode_obat,nama_obat FROM obat")
    obat = cur.fetchall()
    cur.close()
    return jsonify(obat)


# code untuk simpan data pembelian
@app.route('/tambahpembelian', methods=['POST'])
def tambahpembelian():
    if request.method == 'POST':
        no_trans = request.form['no_trans']
        suplier = request.form['suplier']
        jumlah = request.form['net_amount_value']
        date_time = request.form['date_time']
        cur = cnx.cursor()
        cur.execute("INSERT INTO pembelian(kode_transaksi,id_suplier,jumlah,date_time) VALUES(%s,%s,%s,%s)",
                    (no_trans, suplier, jumlah, date_time))
        obat = request.form.getlist('product[]')
        qty = request.form.getlist('qty[]')
        count_product = len(obat)
        jenis = 1
        keluar = 0
        for i in range(count_product):
            cur.execute("INSERT INTO mutasi(kode_transaksi,jenis_transaksi,date_time,id_obat,masuk,keluar) VALUES(%s,%s,%s,%s,%s,%s)",
                        (no_trans, jenis, date_time, obat[i], qty[i], keluar,))
            sql = "UPDATE stok SET stok_akhir = stok_akhir + %s WHERE kode_obat = %s"
            par = (qty[i], obat[i],)
            cur.execute(sql, par)
            cnx.commit()

        cur.close()
        flash("Data Berhasil Ditambahkan")
        return redirect(url_for('pembelian'))


@app.route('/penjualan')  # Menampilkan data penjualan
def penjualan():
    cur = cnx.cursor()
    cur.execute("SELECT id,nama FROM konsumen")
    ks = cur.fetchall()
    cur.execute("SELECT kode_obat,nama_obat FROM obat")
    obat = cur.fetchall()
    cur.execute("SELECT * FROM penjualan")
    jl = cur.fetchall()
    date = datetime.now()
    waktu = date.strftime("%Y-%m-%d")
    cur.close()
    return render_template('penjualan.html', konsumen=ks, ob=obat, date=waktu, jual=jl)


@app.route('/tambahpenjualan', methods=['POST'])
def tambahpenjualan():
    if request.method == 'POST':
        no_trans = request.form['no_trans']
        konsumen = request.form['konsumen']
        jumlah = request.form['net_amount_value']
        date_time = request.form['date_time']
        cur = cnx.cursor()
        cur.execute("INSERT INTO penjualan(kode_transaksi,id_konsumen,jumlah,date_time) VALUES(%s,%s,%s,%s)",
                    (no_trans, konsumen, jumlah, date_time))
        obat = request.form.getlist('product[]')
        qty = request.form.getlist('qty[]')
        count_product = len(obat)
        jenis = 2
        masuk = 0
        for i in range(count_product):
            cur.execute("INSERT INTO mutasi(kode_transaksi,jenis_transaksi,date_time,id_obat,masuk,keluar) VALUES(%s,%s,%s,%s,%s,%s)",
                        (no_trans, jenis, date_time, obat[i], masuk, qty[i]))
            sql = "UPDATE stok SET stok_akhir = stok_akhir - %s WHERE kode_obat = %s"
            par = (qty[i], obat[i],)
            cur.execute(sql, par)
            cnx.commit()

        cur.close()
        flash("Data Berhasil Ditambahkan")
        return redirect(url_for('penjualan'))


if __name__ == "__main__":
    app.run(debug=True)
