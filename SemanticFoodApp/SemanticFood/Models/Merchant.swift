import Foundation

struct Merchant: Hashable, Codable, Identifiable {
      
    var id: String
    var available: Bool
    var currency: String?
    var deliveryInfo: DeliveryInfo?
    var imageUrl: String
    var mainCategory: String
    var name: String
    var userRating: Double
    var description: String
    
    func ifoodLogoUrl() -> String {
        return Constants.ifoodThumbnailUrl + imageUrl.replacingOccurrences(of: ":resolution", with: "")
    }
}

struct DeliveryInfo: Hashable, Codable {
    var type: String?
    var fee: Int?
    var timeMinMinutes: Int?
    var timeMaxMinutes: Int?
}
