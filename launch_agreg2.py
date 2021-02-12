from agregatorAgent import AgregatorAgent

agg2 = AgregatorAgent('agg2')
agg2.startAgregatorReception('localhost',3200,agg2.receive)
agg2.startTransmissionToServer()