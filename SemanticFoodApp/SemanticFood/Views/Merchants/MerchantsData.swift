
import Foundation

class MerchantsViewModel : ObservableObject {
    @Published var recommendations: [Merchant] = []

    func search(name: String) async throws -> [Merchant] {
        var url = URL(string: "http://127.0.0.1:8080/merchants/")!
        
        if(!name.isEmpty)
        {
            url = URL(string: "http://127.0.0.1:8080/merchants/?name=/\(name)")!
        }
        
        
        let (data, _) = try await URLSession.shared.data(from: url)
        
        do {
            let response: Response = try JSONDecoder().decode(Response.self, from: data)
            var merchants = response.textSearch
            merchants.append(contentsOf: response.recommendation)
            
            return merchants
        } catch {
            // Handle decoding errors
            print("Error decoding data: \(error)")
        }
        return [Merchant]()
    }
    
    func get_recommendations(merchantId: String) async throws {
        if(merchantId.isEmpty)
        {
            return
        }
        
        let url = URL(string: "http://127.0.0.1:8080/merchants/\(merchantId)/recommendations")!
        
        URLSession.shared.dataTask(with: url) { data, _, error in
            guard let data = data else {
                return
            }
            do {
                let response: [Merchant] = try JSONDecoder().decode([Merchant].self, from: data)
                DispatchQueue.main.async {
                    self.recommendations = response
                }
            } catch {
                print("Error decoding data: \(error)")
            }
        }.resume()
        
    }
    
    struct Response: Decodable {
        var textSearch: [Merchant]
        var recommendation: [Merchant]
        
        enum CodingKeys: String, CodingKey {
                case textSearch = "text_search"
                case recommendation = "recommendation"
            }
    }
}

