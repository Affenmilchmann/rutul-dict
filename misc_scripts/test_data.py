from pprint import pprint
from check_meanings import check_meanings
from check_unique_labels import check_unique_labels

tests = [{
    'func': check_meanings,
    'info': "Checking meanings integrity...",
    'fail': "Some rows are bad:"
},
{
    'func': check_unique_labels,
    'info': "Checking labels uniquness...",
    'fail': "Some labels are not unique:"
}]

fails = 0

for i, test in enumerate(tests):
    print(f"[{i+1}/{len(tests)}]", test['info'], end=' ')
    out = test['func']()
    if out:
        print()
        print(test['fail'])
        pprint(out)
        fails += 1
    else:
        print('OK')

print(f"{fails} failed\n{len(tests)-fails} succeded")