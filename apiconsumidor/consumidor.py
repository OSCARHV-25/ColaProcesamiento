import sys
import pika
import mysql.connector
import json
import time






def main():
    conexion_bd = {
        'host': 'mysql-soporte-sms',  
        'database': 'sistema_soporte2024',
        'user': 'oscar',
        'password': 'o5592',
        'port': 3306  
    }

  






    while True:
        try:
            conexion_rabbitmq = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-soporte'))
            canal = conexion_rabbitmq.channel()
            canal.queue_declare(queue='cola_soporte')
            print("Conexion exitosa a RabbitMQ")
            break
        except Exception as error:
            print("Error al conectar con RabbitMQ. Reintentando en 5 segundos:", error)
            time.sleep(5)

   







    def procesar_mensaje(ch, method, properties, body):
        cursor = None
        conexion = None
        try:
            datos = json.loads(body)
            nombre = datos['nombre']
            telefono = datos['telefono']
            requerimiento = datos['requerimiento']

            # bd insert
            conexion = mysql.connector.connect(**conexion_bd)
            cursor = conexion.cursor()
            sql = "INSERT INTO requerimiento (nombre, telefono, requerimiento) VALUES (%s, %s, %s)"
            valores = (nombre, telefono, requerimiento)
            cursor.execute(sql, valores)
            conexion.commit()

            print("Requerimiento guardado en la base de datos")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except mysql.connector.Error as error_bd:
            print(f"Error al conectar o insertar en la base de datos: {error_bd}")
        except Exception as error:
            print("Error al procesar el mensaje:", error)
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()


    try:
        canal.basic_consume(queue='cola_soporte', on_message_callback=procesar_mensaje, auto_ack=False)
    except Exception as error:
        print(f"Error al configurar la cola para recibir mensajes: {error}")
        exit(1)

    print('[*] Esperando mensajes. Para salir presione CTRL + C')
    canal.start_consuming()














if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Programa interrumpido')
        sys.exit(0)
