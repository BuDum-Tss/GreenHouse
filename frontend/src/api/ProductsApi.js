import { HttpApi } from './HttpApi';

export class ProductsApi extends HttpApi {
  constructor() {
    super('https://localhost:8000');
    const user = window.Telegram.WebApp.initDataUnsafe?.user;
    const userId = user?.id;
  }

  getProducts(filters) {
    const params = new URLSearchParams(filters).toString();
    return this.sendRequest(`dishes/${userId}?` + params, { method: 'GET' });
  }
}
