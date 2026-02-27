import json
import queue
import time

# Fila simples para despachar alertas de pedidos novos via SSE
alert_queue = queue.Queue()


def publish_alert(data: dict):
    """Publica um alerta na fila."""
    try:
        alert_queue.put_nowait(data)
    except queue.Full:
        # Em caso de fila cheia, descartamos para não travar o fluxo
        pass


def sse_stream():
    """Generator de eventos SSE."""
    while True:
        try:
            payload = alert_queue.get(timeout=30)
        except queue.Empty:
            # envia ping para manter conexão viva
            yield "event: ping\ndata: {}\n\n"
            continue

        yield f"event: pedido\ndata: {json.dumps(payload, default=str)}\n\n"
        time.sleep(0.01)
