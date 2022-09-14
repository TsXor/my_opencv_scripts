# deprecated because it is slow and inaccurate
# also not pythonic ;)
    for z in zones:
        z.draw(showc)
        newbucket = True
        for bucket in bucket_shelf:
            if bucket_check(z, bucket):
                bucket.append(z)
                newbucket = False
                break
        if newbucket:
            abucket = [z]
            bucket_shelf.append(abucket)
# this was added later but was not that meaningful
    orphansidx = [i for i in range(len(bucket_shelf)) if len(bucket_shelf[i])==1]
    eraseorphan = []
    operated = True
    while operated:
        operated = False
        for oi in orphansidx:
            z = bucket_shelf[oi][0]
            for ei in range(len(bucket_shelf)):
                if ei==oi:
                    continue
                bkt = bucket_shelf[ei]
                if bucket_check(z, bkt):
                    operated = True
                    bucket_shelf[ei].append(z)
                    eraseorphan.append(oi)
                    break
        if operated:
            for i in eraseorphan:
                orphansidx.remove(i)
    offset = 0
    for i in eraseorphan:
        bucket_shelf.pop(i+offset)
        offset -= 1