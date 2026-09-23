from app import app, productos
from flask import render_template, redirect, url_for, request
from bson.objectid import ObjectId

# LISTAR
@app.route("/listar")
@app.route("/listarProductos")
def listarProductos():
    listaProductos = productos.find()
    return render_template("listarProductos.html",
                           productos=listaProductos,
                           mensaje="")


# AGREGAR
@app.route("/agregar", methods=["GET", "POST"])
def agregarProducto():
    if request.method == "POST":
        try:
            nuevo = {
                "código": request.form["codigo"],
                "nombre": request.form["nombre"],
                "precio": float(request.form["precio"]),
                "categoría": request.form["categoria"],
                "foto": request.form.get("foto", "")
            }
            productos.insert_one(nuevo)
            mensaje = "Producto agregado correctamente"
        except Exception as error:
            mensaje = f"Error al agregar: {error}"

        listaProductos = productos.find()
        return render_template("listarProductos.html",
                               productos=listaProductos,
                               mensaje=mensaje)
    return render_template("frmAgregarProducto.html")

# CONSULTAR (para editar)
@app.route("/consultar/<idProducto>")
def consultarProducto(idProducto):
    producto = productos.find_one({"_id": ObjectId(idProducto)})
    return render_template("frmEditarProducto.html", producto=producto)

# ACTUALIZAR
@app.route("/actualizar", methods=["POST"])
def actualizarProducto():
    try:
        idProducto = request.form["idProducto"]
        cambios = {
            "código": request.form["codigo"],
            "nombre": request.form["nombre"],
            "precio": float(request.form["precio"]),
            "categoría": request.form["categoria"],
            "foto": request.form.get("foto", "")
        }
        resultado = productos.update_one({"_id": ObjectId(idProducto)}, {"$set": cambios})
        if resultado.modified_count > 0:
            mensaje = "Producto actualizado"
        else:
            mensaje = "No se realizaron cambios"
    except Exception as error:
        mensaje = f"Error al actualizar: {error}"

    listaProductos = productos.find()
    return render_template("listarProductos.html",
                           productos=listaProductos,
                           mensaje=mensaje)

# ELIMINAR
@app.route("/eliminar/<idProducto>")
def eliminarProducto(idProducto):
    try:
        resultado = productos.delete_one({"_id": ObjectId(idProducto)})
        if resultado.acknowledged and resultado.deleted_count > 0:
            mensaje = "Producto eliminado"
        else:
            mensaje = "Problemas al eliminar"
    except Exception as error:
        mensaje = f"Error al eliminar: {error}"

    listaProductos = productos.find()
    return render_template("listarProductos.html",
                           productos=listaProductos,
                           mensaje=mensaje)
