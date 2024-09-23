import logging
import azure.functions as func
import pika

app = func.FunctionApp()

@app.schedule(schedule="", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def poll_queues(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='10.0.4.4',
            port=55672,
            virtual_host='/',  # the virtual host to connect to
            credentials=pika.PlainCredentials('vantage', 'o0j9l2eIwYa96vAQ')
        )
    ) 
    # Create a channel
    channel = connection.channel()
    # Declare the queue (this is idempotent - it won't do anything if the queue already exists)
    queue = channel.queue_declare(queue='vantage')
    # Get the number of messages in the queue
    queue_length = queue.method.message_count
    print(f'The length of the queue is {queue_length}')
    
    # Close the connection
    connection.close()


    logging.info('Python timer trigger function executed.')