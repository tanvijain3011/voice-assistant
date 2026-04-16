import datetime
import winsound

def alarm(Timing):
    alttime = str(datetime.datetime.now().strptime(Timing,"%I:%M %p"))
    
    alttime = alttime[11:-3]
    print(alttime)

    Horeal = alttime[:2]
    Horeal = int(Horeal)
    Mireal = alttime[3:5]
    Mireal = int(Mireal)
    print(f"Done, alarm is set for {Timing}")

    while True:
        if Horeal==datetime.datetime.now().hour:
            if Mireal==datetime.datetime.now().minute:
                print("alarm is running")
                winsound.PlaySound('abc',winsound.SND_LOOP)

            elif Mireal<datetime.datetime.now().minute:
                break

if __name__=='__main__':
    alarm('6:00 PM')