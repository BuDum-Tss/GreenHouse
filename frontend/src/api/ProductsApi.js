import { HttpApi } from './HttpApi';

export class ProductsApi extends HttpApi {
  constructor() {
    super('https://greenhouse-i6s1.onrender.com');
  }

  getProducts(filters) {
    const params = new URLSearchParams(filters).toString();
    return this.sendRequest('dishes?' + params, { method: 'GET' });
  }
}
