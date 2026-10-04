import { Upload } from "lucide-react";

function FileUpload({ platform, accept, file, onFileSelect }) {
  function handleChange(event) {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      onFileSelect(selectedFile);
    }
  }

  return (
    <label className="file-upload">
      <input
        type="file"
        accept={accept}
        onChange={handleChange}
        hidden
      />

      <div className="upload-icon">
        <Upload size={22} />
      </div>

      <div className="upload-content">
        <span className="upload-platform">{platform}</span>

        {file ? (
          <span className="upload-file">{file.name}</span>
        ) : (
          <>
            <span className="upload-description">
              Drop your export here
            </span>

            <span className="upload-action">
              Choose file
            </span>
          </>
        )}
      </div>
    </label>
  );
}

export default FileUpload;