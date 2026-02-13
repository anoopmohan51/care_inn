from workorder_api.models.rooms import Rooms
from workorder_api.models.patient_mrn import Mrn

def _update_mrn(mrd_id,room_number):
    try:
        mrn = Mrn.objects.get(mrn=mrd_id)
        if mrn:
            room = Rooms.objects.get(room_number=room_number,is_delete=False)
            if room:
                room.mrn = mrn
                room.save()
                return True
        return False
    except Exception as e:
        return False