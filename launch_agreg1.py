from aggregatorAgent import AggregatorAgent

agg = AggregatorAgent('agg1')
agg.startAgregatorReception('localhost',3100,agg.receive)
agg.startTransmissionToServer()