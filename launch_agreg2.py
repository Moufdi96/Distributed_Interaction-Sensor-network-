from aggregatorAgent import AggregatorAgent

agg2 = AggregatorAgent('agg2')
agg2.startAgregatorReception('localhost',3200,agg2.receive)
agg2.startTransmissionToServer()