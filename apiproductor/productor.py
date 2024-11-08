import pika
from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)









while True:
    try:
        conexion = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq_servicio'))
        canal = conexion.channel()
        canal.queue_declare(queue='cola_soporte')
        print("Conexion exitosa a RabbitMQ")
        conexion.close()  
        break
    except Exception as error:
        print("Error al conectar con RabbitMQ. Reintentando en 5 segundos:", error)
        time.sleep(5)





@app.route('/soporte', methods=['POST'])
def recibir_solicitud():
    datos = request.get_json()
    cliente_nombre = datos.get('nombre')
    cliente_telefono = datos.get('telefono')
    cliente_requerimiento = datos.get('requerimiento')






    if not cliente_nombre or not cliente_telefono or not cliente_requerimiento:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    solicitud = {
        "nombre": cliente_nombre,
        "telefono": cliente_telefono,
        "requerimiento": cliente_requerimiento
    }

    try:
        
        conexion = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq_servicio'))
        canal = conexion.channel()
        canal.queue_declare(queue='cola_soporte') 
        
         


        
        canal.basic_publish(
            exchange='',
            routing_key='cola_soporte',
            body=json.dumps(solicitud),
            properties=pika.BasicProperties(delivery_mode=2) 
        )
        
       
        conexion.close()  
        print("Mensaje enviado a la cola con exito")
        return jsonify({"mensaje": "Solicitud de soporte recibida"}), 201

    except Exception as error:
        print("Error al enviar el mensaje:", error)
        return jsonify({"error": "No se pudo enviar el mensaje a la cola"}), 500










if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
