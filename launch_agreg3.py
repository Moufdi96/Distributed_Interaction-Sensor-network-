from agregatorAgent import AgregatorAgent

agg3 = AgregatorAgent('agg3')
agg3.startAgregatorReception('localhost',3300,agg3.receive)
agg3.startTransmissionToServer()