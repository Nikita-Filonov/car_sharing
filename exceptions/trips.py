class TripAlreadyStarted(Exception):
    pass


class TransportAlreadyReserved(Exception):
    pass


class ForbiddenToBookTransport(Exception):
    pass


class UnknownTripPriceType(Exception):
    pass
