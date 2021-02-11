from aggregatorAgent import AggregatorAgent

agg3 = AggregatorAgent('agg3')
agg3.startAgregatorReception('localhost',3300,agg3.receive)
agg3.startTransmissionToServer()