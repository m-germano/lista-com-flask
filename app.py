from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///listadecompras2.db"

db=SQLAlchemy(app)
class databaseProjeto(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    produto=db.Column(db.String(50))
    marca=db.Column(db.String(50))
    quantidade=db.Column(db.Integer)
    preco=db.Column(db.Float)

    def __init__(self, produto, marca, quantidade, preco):
        self.produto=produto
        self.marca=marca
        self.quantidade=quantidade
        self.preco=preco


@app.route('/', methods=['POST', 'GET'])
def principal():
    page=request.args.get('page', 1, type=int)
    per_page=10
    lista=databaseProjeto.query.paginate(page=page, per_page=per_page)
    return render_template('index.html', lista=lista)

@app.route('/adicionar_produto',methods=['POST', 'GET'])
def adicionar_produto():
    produto=request.form.get('produto')
    marca=request.form.get('marca')
    quantidade=request.form.get('quantidade')
    preco=request.form.get('preco')
    
    if request.method =='POST':
        if not produto or not marca or not quantidade or not preco:
            flash("Preencha todos os campos do formulario", "error")
        nova_lista=databaseProjeto(produto, marca, quantidade, preco)
        db.session.add(nova_lista)
        db.session.commit()
        return redirect(url_for('principal'))
    return render_template('adicionar_produto.html')

@app.route('/<int:id>/editar',methods=['POST', 'GET'])
def editar(id):
    produtos=databaseProjeto.query.filter_by(id=id).first()
    if request.method=='POST':
        produto=request.form.get('produto')
        marca=request.form.get('marca')
        quantidade=request.form.get('quantidade')
        preco=request.form.get('preco')
        #######################################################
        databaseProjeto.query.filter_by(id=id).update({'produto':produto, 'marca':marca, 'quantidade':quantidade, 'preco':preco })
        db.session.commit()
        return redirect(url_for('principal'))
    return render_template('editar.html', item=produtos)






@app.route('/<int:id>/remover')
def remover(id):
    item_a_deletar=databaseProjeto.query.filter_by(id=id).first()
    db.session.delete(item_a_deletar)
    db.session.commit()
    return redirect(url_for('principal'))


with app.app_context():   
 db.create_all()

if __name__=="__main__":
    app.run(debug=True)
