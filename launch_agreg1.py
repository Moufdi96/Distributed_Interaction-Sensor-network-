from agregatorAgent import AgregatorAgent

agg1 = AgregatorAgent('agg1')
agg1.startAgregatorReception('localhost',3100,agg1.receive)
agg1.startTransmissionToServer()

