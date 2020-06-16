from kalyna_dstu import kalyna


def test_dstu():
    key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]

    k = kalyna.Kalyna(key)

    k.encryption("message.txt", "message_encrypted.txt")
    k.decryption("message_encrypted.txt", "message_decrypted.txt")


if __name__ == '__main__':
    test_dstu()
