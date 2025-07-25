const DEFAULT_ERROR = 'Не удалось выполнить запрос.';

export class HttpApi {
  constructor(baseUrl) {
    this._baseUrl = baseUrl;
  }

  _getError(response) {
    return response.json().then((error) => Promise.reject(error?.message || DEFAULT_ERROR));
  }

  _checkResponse(response) {
    if (response.ok) {
      return response.json();
    }
    return this._getError(response);
  }

  sendRequest(endpoint, options) {
    return fetch(`${this._baseUrl}/${endpoint}`, options).then((response) => this._checkResponse(response));
  }
}
