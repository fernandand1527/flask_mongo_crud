from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a MongoDB
from pymongo import MongoClient

# Conexión a MongoDB Atlas
from pymongo import MongoClient

from pymongo import MongoClient

from pymongo import MongoClient

from pymongo import MongoClient

cliente = MongoClient("mongodb+srv://fernandand1527_db_user:Fer34319194*@cluster0.k0cpyhn.mongodb.net/GESTIONPRODUCTOS?retryWrites=true&w=majority")
db = cliente["GESTIONPRODUCTOS"]
productos = db["PRODUCTOS"]



# LISTAR
@app.route("/")
@app.route("/listarProductos")
def listarProductos():
    lista = list(productos.find())
    return render_template("listarProductos.html", productos=lista)


# AGREGAR
@app.route("/agregarProducto", methods=["GET", "POST"])
def agregarProducto():
    if request.method == "POST":
        nuevo = {
            "código": request.form["codigo"],
            "nombre": request.form["nombre"],
            "precio": float(request.form["precio"]),
            "categoría": request.form["categoria"],
            "foto": request.form.get("foto", "")
        }
        productos.insert_one(nuevo)
        return redirect(url_for("listarProductos"))
    return render_template("frmAgregarProducto.html")

# CONSULTAR (para editar)
@app.route("/consultar/<idProducto>")
def consultarProducto(idProducto):
    producto = productos.find_one({"_id": ObjectId(idProducto)})
    return render_template("frmEditarProducto.html", producto=producto)

# ACTUALIZAR
@app.route("/actualizarProducto", methods=["POST"])
def actualizarProducto():
    idProducto = request.form["id"]
    productos.update_one(
        {"_id": ObjectId(idProducto)},
        {"$set": {
            "código": request.form["codigo"],
            "nombre": request.form["nombre"],
            "precio": float(request.form["precio"]),
            "categoría": request.form["categoria"],
            "foto": request.form.get("foto", "")
        }}
    )
    return redirect(url_for("listarProductos"))

# ELIMINAR
@app.route("/eliminarProducto/<idProducto>")
def eliminarProducto(idProducto):
    productos.delete_one({"_id": ObjectId(idProducto)})
    return redirect(url_for("listarProductos"))

if __name__ == "__main__":
    app.run(port=3000, debug=True)
