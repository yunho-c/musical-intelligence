from spatial_env.head_tracker import HeadTracker

ht = HeadTracker()

ht.start()
while True:
    res = ht.step()
    # if res == -1: break
    # else: print(res)
    try: print(res.round(2))
    except Exception as e: print(e)
ht.end()

