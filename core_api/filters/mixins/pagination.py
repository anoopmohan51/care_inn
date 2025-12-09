class PaginationMixin:
    def _positive_int(self, integer_string, strict=False, cutoff=None):
        ret = int(integer_string)
        if ret < 0 or (ret == 0 and strict):
            raise ValueError()
        if cutoff:
            return min(ret, cutoff)
        return ret
    
    def get_limit(self):
        try:
            return self._positive_int(self.request.query_params.get('limit', -1), strict=True, cutoff=1000)
        except (ValueError, TypeError):
            return -1

    def get_offset(self):
        try:
            return self._positive_int(self.request.query_params.get('offset', 0))
        except (ValueError, TypeError):
            return 0