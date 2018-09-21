from intaller import check_CPUsum, get_CPUsum


if __name__ == "__main__":
    is_have_license = check_CPUsum(get_CPUsum())

    if is_have_license:
        print("Cool! You have a license!")
    else:
        print("Sorry, access is denied!")

