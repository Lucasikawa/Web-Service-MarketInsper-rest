from flask import Flask, request
import psycopg2
import json

app = Flask("MarketInsper_teste")

conn = psycopg2.connect(
    dbname="mbgtffgx",
    user="mbgtffgx",
    password="LCpXnqn773po70nuSkreWfuooS3b7Ul3",
    host="kesavan.db.elephantsql.com"
)

@app.route('/')
def wellcome_mktinsper():
    return "Seja bem vindo ao MarketInsper"

@app.route('/candidatos', methods=['POST'])
def create_candidato():
    dic_candidato = request.json
    nome = dic_candidato.get('nome', "")
    email_insper = dic_candidato.get('email_insper', "")
    curso = dic_candidato.get('curso', "")
    semestre = dic_candidato.get('semestre', 0)
    
    if not nome or not email_insper or not curso or not semestre:
        return {"mensagem": "Faltou informar algum campo"}, 400
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO candidatos (nome, email_insper, curso, semestre) VALUES (%s, %s, %s, %s)", (nome, email_insper, curso, semestre))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    resp = {
        "mensagem": "Candidato cadastrado",
        "candidato": dic_candidato
    }
    return resp, 201

@app.route('/candidatos', methods=['GET'])
def show_canditos():
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM candidatos")
        candidatos = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    lista_candidatos = []
    for candidato in candidatos:
        lista_candidatos.append({
            "id": candidato[0],
            "nome": candidato[1],
            "email_insper": candidato[2],
            "curso": candidato[3],
            "semestre": candidato[4]
        })

    return lista_candidatos

@app.route('/candidato/delete/<int:id_candidato>', methods=['DELETE'])
def delete_candidato(id_candidato):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM candidatos WHERE id = %s", (id_candidato,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 400
    finally:
        cur.close()
    return {"mensagem": "Candidato deletado com sucesso"}

@app.route('/projetos', methods=['POST'])
def create_projetos():
    dic_projeto = request.json
    empresa = dic_projeto.get("empresa", "")
    qnt_pessoas = dic_projeto.get("qnt_pessoas", 0)
    core = dic_projeto.get("core")
    dedline = dic_projeto.get("dedline")

    if not empresa or not qnt_pessoas or not core or not dedline:
        return {"mensagem": "Falta preencher algum campo"}, 400
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO projetos (empresa, qnt_pessoas, core, dedline) VALUES (%s, %s, %s, %s)", (empresa, qnt_pessoas, core, dedline))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    resp = {
        "mensagem": "Candidato cadastrado",
        "projeto": dic_projeto
    }
    return resp, 201

@app.route('/projetos/<int:id_projeto>', methods=['PUT'])
def altera_projeto(id_projeto):
    dic_projeto = request.json
    empresa = dic_projeto.get("empresa", "")
    qnt_pessoas = dic_projeto.get("qnt_pessoas", 0)
    core = dic_projeto.get("core", "")
    dedline = dic_projeto.get("dedline", "")

    if not empresa or qnt_pessoas or core or dedline:
        return {"mensagem": "Faltou informar algum campo"}
    
    try:
        cur = conn.cursor()
        cur.execute("UPDATE projetos SET empresa = %s, qnt_pessoas = %s, core = %s, dedline = %s", (empresa, qnt_pessoas, core, dedline))
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    resp = {
        "mensagem": "Projeto atualizado com sucesso",
        "projeto": dic_projeto
    }
    return resp, 200



if __name__ == "__main__":
    app.run(debug=True)