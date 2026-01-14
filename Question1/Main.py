# Import the string module to easily access alphabet letters
import string


def encrypt_character(char, key1, key2):
    """
    Encrypts a single character based on:
    - whether it is lowercase or uppercase
    - the given key values (key1 and key2)
    """

    # Check if the character is a lowercase letter
    if char.islower():

        # Check if the character is in the lowercase alphabet
        # (intended for first half of the alphabet)
        if char in "abcdefghijklmnopqrstuvwxyz":
            # Calculate the shift using multiplication of keys
            offset = key1 * key2

            # Store all lowercase letters
            letters = string.ascii_lowercase

            # Encrypt by shifting forward in the alphabet
            return letters[(letters.index(char) + offset) % 26]

        else:
            # For the second half of lowercase letters
            offset = key1 + key2
            letters = string.ascii_lowercase

            # Encrypt by shifting backward in the alphabet
            return letters[(letters.index(char) - offset) % 26]

   
    # Check if the character is an uppercase letter
    elif char.isupper():

        # Check if the character is in the uppercase alphabet
        # (intended for first half of the alphabet)
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            # Use key1 as the shift value
            offset = key1

            # Store all uppercase letters
            letters = string.ascii_uppercase

            # Encrypt by shifting backward
            return letters[(letters.index(char) - offset) % 26]

        else:
            # For the second half of uppercase letters
            offset = key2 ** 2
            letters = string.ascii_uppercase

            # Encrypt by shifting forward
            return letters[(letters.index(char) + offset) % 26]

 
    # If the character is not a letter (space, number, punctuation, etc.)
    else:
        # Return the character unchanged
        return char


def encrypt_file(key1, key2):
    """
    Reads text from 'raw_text.txt',
    encrypts it character by character,
    and saves the result in 'encrypted_text.txt'
    """

    # Open the original file in read mode
    with open("raw_text.txt", "r", encoding="utf-8") as input_file:
        # Read the full content of the file
        original_text = input_file.read()

    # Encrypt each character using encrypt_character()
    cipher_text = "".join(
        encrypt_character(char, key1, key2) for char in original_text
    )

    # Open the encrypted file in write mode
    with open("encrypted_text.txt", "w", encoding="utf-8") as output_file:
        # Write the encrypted text to the file
        output_file.write(cipher_text)


def decrypt_character(char, key1, key2):
    """
    Decrypts a single character by reversing
    the encryption logic using the same keys
    """

    # Check if the character is lowercase
    if char.islower():

        # Intended first half of lowercase letters
        if char in "abcdefghijklmnopqrstuvwxyz":
            offset = key1 * key2
            letters = string.ascii_lowercase

            # Reverse the encryption shift
            return letters[(letters.index(char) - offset) % 26]

        else:
            # Second half of lowercase letters
            offset = key1 + key2
            letters = string.ascii_lowercase

            # Reverse backward shift by moving forward
            return letters[(letters.index(char) + offset) % 26]

    # Check if the character is uppercase
    elif char.isupper():

        # Intended first half of uppercase letters
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            offset = key1
            letters = string.ascii_uppercase

            # Reverse backward shift by moving forward
            return letters[(letters.index(char) + offset) % 26]

        else:
            # Second half of uppercase letters
            offset = key2 ** 2
            letters = string.ascii_uppercase

            # Reverse forward shift by moving backward
            return letters[(letters.index(char) - offset) % 26]

    # If the character is not a letter
    else:
        # Return it unchanged
        return char


def decrypt_file(key1, key2):
    """
    Reads encrypted text from 'encrypted_text.txt',
    decrypts it,
    and saves the result in 'decrypted_text.txt'
    """

    # Open the encrypted file in read mode
    with open("encrypted_text.txt", "r", encoding="utf-8") as input_file:
        # Read the encrypted content
        cipher_text = input_file.read()

    # Decrypt each character using decrypt_character()
    plain_text = "".join(
        decrypt_character(char, key1, key2) for char in cipher_text
    )

    # Open the decrypted file in write mode
    with open("decrypted_text.txt", "w", encoding="utf-8") as output_file:
        # Write the decrypted text to the file
        output_file.write(plain_text)


def verify():
    """
    Verifies whether decryption was successful
    by comparing original and decrypted files
    """

    # Open both original and decrypted files
    with open("raw_text.txt", "r", encoding="utf-8") as file1, \
         open("decrypted_text.txt", "r", encoding="utf-8") as file2:

        # Read contents of both files
        original = file1.read()
        decrypted = file2.read()

    # Compare the contents
    if original == decrypted:
        print("Decryption successful! Files match.")
    else:
        print("Decryption failed! Files do not match.")


def main():
    """
    Main function that controls the program flow
    """

    # Ask the user to enter key values
    key1 = int(input("Enter shift1 value: "))
    key2 = int(input("Enter shift2 value: "))

    # Encrypt the original file
    print("Encrypting the raw_text.txt file...")
    encrypt_file(key1, key2)

    # Decrypt the encrypted file
    print("Decrypting the encrypted_text.txt file...")
    decrypt_file(key1, key2)

    # Verify if decryption worked correctly
    print("Verifying...")
    verify()


# Run the program only if this file is executed directly
if __name__ == "__main__":
    main()
