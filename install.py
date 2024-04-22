import launch

if not launch.is_installed("face_recognition"):
    print('Installing requirements for SimilaritySifter')
    launch.run_pip("install face_recognition", "requirements for face_recognition")