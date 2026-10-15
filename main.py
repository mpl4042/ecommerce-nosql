from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Conexão MongoDB Atlas
client = MongoClient("mongodb+srv://michelelima02_db_user:suRHYYatjmspbCum@cluster0.w0n6us0.mongodb.net/ecommerce?retryWrites=true&w=majority&appName=Cluster0")
db = client['ecommerce']
produtos_collection = db['produtos']

# CREATE
@app.route('/produtos', methods=['POST'])
def adicionar_produto():

    novo_produto = request.get_json()

    produto_id = produtos_collection.insert_one(novo_produto).inserted_id

    return jsonify({
        "mensagem": "Produto adicionado com sucesso!",
        "id": str(produto_id)
    }), 201

# READ
@app.route('/produtos', methods=['GET'])
def listar_produtos():

    produtos = list(produtos_collection.find())

    for produto in produtos:
        produto['_id'] = str(produto['_id'])

    return jsonify(produtos)

# READ por ID
@app.route('/produtos/<id>', methods=['GET'])
def obter_produto(id):

    produto = produtos_collection.find_one({
        "_id": ObjectId(id)
    })

    if produto:

        produto['_id'] = str(produto['_id'])

        return jsonify(produto)

    return jsonify({
        "erro": "Produto não encontrado"
    }), 404

# UPDATE
@app.route('/produtos/<id>', methods=['PUT'])
def atualizar_produto(id):

    dados_atualizados = request.get_json()

    resultado = produtos_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": dados_atualizados}
    )

    if resultado.matched_count > 0:

        return jsonify({
            "mensagem": "Produto atualizado com sucesso!"
        })

    return jsonify({
        "erro": "Produto não encontrado"
    }), 404

# DELETE
@app.route('/produtos/<id>', methods=['DELETE'])
def remover_produto(id):

    resultado = produtos_collection.delete_one({
        "_id": ObjectId(id)
    })

    if resultado.deleted_count > 0:

        return jsonify({
            "mensagem": "Produto removido com sucesso!"
        })

    return jsonify({
        "erro": "Produto não encontrado"
    }), 404



if __name__ == '__main__':
    app.run(debug=True)