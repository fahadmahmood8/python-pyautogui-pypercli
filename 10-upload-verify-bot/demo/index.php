<?php
// Tiny upload handler for testing the bot on WAMP.
// Copy the "demo" folder to C:\wamp64\www\upload-demo and open http://localhost/upload-demo/
$dir = __DIR__ . '/uploads/';
if (!is_dir($dir)) {
    mkdir($dir, 0777, true);
}

$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    if ($_FILES['file']['error'] === UPLOAD_ERR_OK) {
        $name = basename($_FILES['file']['name']);
        move_uploaded_file($_FILES['file']['tmp_name'], $dir . $name);
        $message = 'Uploaded: ' . htmlspecialchars($name);
    } else {
        $message = 'Upload error code: ' . (int) $_FILES['file']['error'];
    }
}
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Upload Demo</title>
  <style>
    body { font-family: system-ui, sans-serif; padding: 40px; }
    .msg { margin-top: 16px; padding: 10px; background: #dcfce7; border-radius: 6px; display: inline-block; }
  </style>
</head>
<body>
  <h1>Upload Demo</h1>
  <form method="post" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">Upload</button>
  </form>
  <?php if ($message): ?>
    <div class="msg"><?= $message ?></div>
  <?php endif; ?>
</body>
</html>
