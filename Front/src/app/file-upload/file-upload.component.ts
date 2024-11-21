import { Component } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent {
  selectedFile: File | null = null;
  predictionResult: string = '';
  errorMessage: string = '';

  constructor(private http: HttpClient) {}

  onFileSelected(event: any): void {
    if (event.target.files && event.target.files.length > 0) {
      this.selectedFile = event.target.files[0];
    }
  }

  onUpload(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Please select a file first!';
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<{ genre: string }>('http://127.0.0.1:1000/predict', formData)
      .subscribe({
        next: (response) => {
          this.predictionResult = `Predicted genre: ${response.genre}`;
          this.errorMessage = '';
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage = `Error: ${error.message}`;
          this.predictionResult = '';
        }
      });
  }
}
