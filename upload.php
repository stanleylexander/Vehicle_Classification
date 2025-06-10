<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Upload and Predict Vehicle Image</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .content {
            flex: 1;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        #header-title {
            flex: 1;
            text-align: center;
            color: white;
            font-size: 20px;
        }
    </style>
</head>
<body>
    <div class="mb-3">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <img src="Logo/ubaya.png" alt="Logo" style="max-width: 100px; height: 100px;">
                <p id="header-title" class="mb-0">VEHICLE CLASSIFIER</p>
            </div>
        </nav>
    </div>

    <div class="content">
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-lg-6">
                    <div class="card">
                        <div class="card-header text-center">
                            <h2>Upload Vehicle Image for Prediction</h2>
                        </div>
                        <div class="card-body">
                            <form action="upload.php" method="post" enctype="multipart/form-data">
                                <div class="form-group">
                                    <label for="fileToUpload">Select image to upload:</label>
                                    <input type="file" class="form-control-file" name="fileToUpload" id="fileToUpload" required>
                                </div>
                                <button type="submit" class="btn btn-primary btn-block">Upload Image</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <?php
            if ($_SERVER['REQUEST_METHOD'] == 'POST') {
                $target_dir = "uploads/";
                
                if (!file_exists($target_dir)) {
                    mkdir($target_dir, 0777, true);
                }

                $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
                $uploadOk = 1;
                $imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

                $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
                if ($check !== false) {
                    echo '<div class="row justify-content-center mt-3"><div class="col-lg-6 text-center">';
                    echo "File is an image - " . $check["mime"] . ".<br>";
                    $uploadOk = 1;
                } else {
                    echo '<div class="row justify-content-center mt-3"><div class="col-lg-6 text-center">';
                    echo "File is not an image.<br>";
                    $uploadOk = 0;
                }

                if (file_exists($target_file)) {
                    echo "Sorry, file already exists.<br>";
                    $uploadOk = 0;
                }

                if ($_FILES["fileToUpload"]["size"] > 50000000) {
                    echo "Sorry, your file is too large.<br>";
                    $uploadOk = 0;
                }

                if ($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg" && $imageFileType != "gif") {
                    echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.<br>";
                    $uploadOk = 0;
                }

                if ($uploadOk == 0) {
                    echo "Sorry, your file was not uploaded.<br>";
                } else {
                    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
                        echo "The file ". basename($_FILES["fileToUpload"]["name"]). " has been uploaded.<br>";

                        $command = escapeshellcmd("python predict.py " . escapeshellarg($target_file));
                        $output = shell_exec($command . " 2>&1");

                        if ($output === null) {
                            echo "Error executing Python script.<br>";
                        } else {
                            list($prediction, $confidence, $sobel_image_path, $hog_image_path, $combined_image_path) = explode(",", trim($output));
                            echo "Predicted class: $prediction<br>";
                            echo "Confidence: $confidence%<br>";

                            $accuracy_file = 'C:/xampp/htdocs/phpscript/Project DIP/accuracy.txt';
                            if (file_exists($accuracy_file)) {
                                $accuracy = file_get_contents($accuracy_file);
                                echo "Model Accuracy: $accuracy%<br>";
                            }

                            echo '</div></div>';  

                            echo '<div class="row justify-content-center mt-3"><div class="col-lg-10 text-center">';
                            echo "<img src='".basename($combined_image_path)."' alt='Combined Image'><br>";
                            echo '</div></div>'; 
                        }
                    } else {
                        echo "Sorry, there was an error uploading your file.<br>";
                    }
                }

                echo '</div></div>';
            }
            ?>
        </div>
    </div>

    <div class="mt-auto">
        <footer class="bg-dark text-white text-center py-3">
            <div class="container">
                <p class="mb-0">Kelompok 1</p>
                <p class="mb-0">by James, Matthew, Oakley, Stanley</p>
            </div>
        </footer>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
