from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

#desarrollando la interfaz gráfica
root=Tk()
root.title ("usuarios")
root.geometry("600x350")

#las variables de los usuarios

elID=StringVar()
elNombre=StringVar()
elCorreo=StringVar()
elUsuario=StringVar()
laContraseña=StringVar()

#la conexion con la base de datos sirve para crear y conectar con la base

def conexiondb():
    laConexion=sqlite3.connect("usuarios")
    elCursor=laConexion.cursor()
    
    try:
        elCursor.execute('''
            CREATE TABLE  usuarios (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR NOT NULL,
            CORREO VARCHAR NOT NULL,
            USUARIO VARCHAR NOT NULL,
            CONTRASEÑA VARCHAR NOT NULL)             
             ''')
        messagebox.showinfo("CONEXION","base de datos creada con exito")
    except:
        messagebox.showinfo("CONEXION","conexion m exitosa con db")
        
        

           
        
def eliminardb():
    laConexion=sqlite3.connect("usuarios")
    elCursor=laConexion.cursor()
    if messagebox.askyesno(message="¿los datos se perderan definitivamente, desea continuar?",title="Advertencia" ):
       elCursor.execute("DROP TABLE usuarios")
    else:
        pass
       
       
def salirAplicacion():    
    valor=messagebox.askquestion("salir","¿Esta seguro que desea salir")
    if valor=="yes":
        root.destroy()
        

#setea las cajas de texto una vez se carga           
        
def limpiarCampos():
    elID.set("")
    elNombre.set("")
    elCorreo.set("")
    elUsuario.set("")
    laContraseña.set("")
    
def mensaje():
    acerca='''
    Aplicacion CRUD
    version 1.0
    Tecnologia Python Tkinter
    '''
#metodos Crud

def crear():
    laConexion=sqlite3.connect("usuarios")
    elCursor=laConexion.cursor()
    try:
        datos=elNombre.get(),elCorreo.get(),elUsuario.get(),laContraseña.get()
        elCursor.execute("INSERT INTO usuarios VALUES(NULL,?,?,?,?)",(datos))
        laConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","OCURRIO UN ERROR AL CREAR EL REGISTRO VERIFIQUE CONEXION CON BASE DE DATOS") 
        pass
    limpiarCampos()
    mostrar()   
    
def mostrar():
    laConexion=sqlite3.connect("usuarios")
    elCursor=laConexion.cursor()
    registros=tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        elCursor.execute("SELECT * FROM usuarios")
        for row in elCursor:
            tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4]))
    except:
        pass
    
#crear tabla

tree=ttk.Treeview(height=10,columns=('#0','#1','#2','#3'))
tree.place(x=0, y=130)
tree.column('#0',width=100)
tree.heading('#0',text="ID",anchor=CENTER)
tree.heading("#1",text="Nombre",anchor=CENTER)
tree.heading("#2",text="Correo electronico",anchor=CENTER)
tree.heading("#3",text="Usuario",anchor=CENTER)
tree.heading("#4",text="Contraseña",anchor=CENTER)



def eventoclick(event):
    item=tree.identify('item',event.x,event.y)
    elID.set(tree.item(item,"text"))
    elNombre.set(tree.item(item,"values")[0])
    elCorreo.set(tree.item(item,"values")[1])
    elUsuario.set(tree.item(item,"values")[2])
    laContraseña.set(tree.item(item,"values")[3])
tree.bind("<Double-1>", eventoclick)




def actualizar():
    laConexion=sqlite3.connect("usuarios")
    elCursor=laConexion.cursor()
    try:
        datos=elNombre.get(),elCorreo.get(),elUsuario.get(),laContraseña.get()
        elCursor.execute("UPDATE usuarios SET NOMBRE=?,CORREO=?,USUARIO=?,CONTRASEÑA=? WHERE ID="+ elID.get(),(datos))
        laConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","OCURRIO UN ERROR AL ACTUALIZAR EL REGISTRO VERIFIQUE CONEXION CON BASE DE DATOS") 
        pass
    limpiarCampos()
    mostrar()   
    
def borrar():
    laConexion=sqlite3.connect("usuarios")
    elCursor=laConexion.cursor()
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?",title="advertencia"):
            elCursor.execute("DELETE FROM usuarios WHERE ID=" + elID.get())
            laConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","OCURRIO UN ERROR AL TRATAR DE ELIMINAR EL REGISTRO")  
        pass
    limpiarCampos()
    mostrar()          
    
#colocar widget

#creacion de menu
menubar=Menu (root)
menubasedat=Menu(menubar,tearoff=0) 
menubasedat.add_command(label="crear/conectar base de datos", command=conexiondb) 
menubasedat.add_command(label="Eliminar base de datos", command=eliminardb)

menubasedat.add_command(label="salir de base de datos", command=salirAplicacion) 
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu=Menu(menubar,tearoff=0)
ayudamenu.add_command(label="resetear campos", command=limpiarCampos) 
ayudamenu.add_command(label="acerca", command=mensaje) 
menubar.add_cascade(label="ayuda",menu=ayudamenu)

#etiquetas y cajas de texto

e1=Entry(root,textvariable=elID)

l2=Label(root,text="Nombre")
l2.place(x=50,y=10)
e2=Entry(root,textvariable=elNombre,width=50)
e2.place(x=100,y=10) 


l3=Label(root,text="Correo electronico")
l3.place(x=50,y=30)
e3=Entry(root,textvariable=elCorreo,width=50)
e3.place(x=150,y=30)

l4=Label(root,text="usuario")
l4.place(x=50,y=50)
e4=Entry(root,textvariable=elUsuario,width=50)
e4.place(x=100,y=50)

l5=Label(root,text="contraseña")
l5.place(x=90,y=70)
e5=Entry(root,textvariable=laContraseña,width=50)
e5.place(x=150,y=70)

#botones
b1=Button(root,text="crear registro",command=crear)
b1.place(x=50,y=90)
b2=Button(root,text="modificar registro",command=actualizar)
b2.place(x=180,y=90)
b3=Button(root,text="mostrar lista",command=mostrar)
b3.place(x=320,y=90)
b4=Button(root,text="eliminar registro", bg="red",command=borrar)
b4.place(x=450,y=90)



root.config(menu=menubar)
 
#esta siempre esperando, sirve para ver la tabla cuando se indique
root.mainloop()
    
      
           
            
