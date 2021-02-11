from aggregatorAgent import AggregatorAgent

agg1 = AggregatorAgent('agg1')
agg1.startAgregatorReception('localhost',3100,agg1.receive)
agg1.startTransmissionToServer()

