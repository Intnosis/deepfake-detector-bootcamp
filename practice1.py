test_1 = ['a.jpg', 'b.png', ' C.JPG']
test_2 = ['photo.JPG', 'photo2.jpeg', 'image.PNG', 'dog.jpg']
test_3 = ['hello.txt', 'test.docx', 'notes.pdf']


def count_test(counting):
    count = 0

    for test in counting:
        if test.lower().endswith('jpg'):
            count += 1
            
    return count

print('Test 1:',test_1)
print('JPG count:',count_test(test_1))
print('\n')
print('Test 2:', test_2)
print('JPG count:',count_test(test_2))
print('\n')
print('Test 3:', test_3)
print('JPG count:',count_test(test_3))