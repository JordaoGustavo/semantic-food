
import SwiftUI

struct MerchantRow: View {
    var merchant: Merchant
    
    
    var body: some View {
        let minTime = String(merchant.deliveryInfo?.timeMinMinutes ?? 0)
        let maxTime = String(merchant.deliveryInfo?.timeMaxMinutes ?? 0)
        let hasDeliveryInfo = merchant.deliveryInfo != nil
        let fullFee: Double = Double(merchant.deliveryInfo?.fee ?? 0) / 100
        
        HStack {
            AsyncImage(url: URL(string: merchant.ifoodLogoUrl())) { phase in
                switch phase {
                case .empty:
                    ProgressView()
                case .success(let image):
                    image
                        .resizable()
                        .frame(width: 75, height: 75)
                case .failure:
                    Image(systemName: "photo")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                @unknown default:
                    EmptyView()
                }
            }
            VStack(alignment: .leading) {
                Text(merchant.name)
                    .bold()
                    .font(.system(size: 20))
                    .foregroundColor(.black)
                HStack(spacing: 10) {
                    Text(String(format: "%.2f", merchant.userRating))
                        .foregroundColor(.yellow)
                    Text("*")
                        .foregroundStyle(.gray)
                    Text(merchant.mainCategory)
                        .foregroundStyle(.gray)
                }
                .font(.system(size: 18))
                HStack(spacing: 10) {
                    if(hasDeliveryInfo) {
                        Text(minTime + "-" + maxTime + " min")
                            .foregroundStyle(.gray)
                    }
                    Text("*")
                        .foregroundStyle(.gray)
                    fullFee == 0 ? 
                    Text("Gratis")
                        .foregroundStyle(.green):
                    Text("R$ " + String(format: "%.2f", fullFee))
                        .foregroundStyle(.gray)
                }.padding(1)
                .font(.system(size: 18))
            }
        }.padding()
    }
}

#Preview {
    Group {
        MerchantRow(merchant: Merchant(id: UUID().uuidString, available: true, currency: "BRL", deliveryInfo: DeliveryInfo(type: "Delivery", fee: 120, timeMinMinutes: 55, timeMaxMinutes: 120), imageUrl: "logosgde/06448d05-5295-498d-bf4c-6fad4d37d69b_PAGUE_OJA03.png",  mainCategory: "Lanches", name: "Pague Menos - Av Cillos - Loja 03", userRating: 4.645, description: "Lanches do Dedao"))
        MerchantRow(merchant: Merchant(id: UUID().uuidString, available: true, currency: "BRL", deliveryInfo: DeliveryInfo(type: "Delivery", fee: 120, timeMinMinutes: 55, timeMaxMinutes: 120), imageUrl: "logosgde/06448d05-5295-498d-bf4c-6fad4d37d69b_PAGUE_OJA03.png",  mainCategory: "Lanches", name: "Pague Menos - Av Cillos - Loja 03", userRating: 4.645, description: "Lanches do Dedao"))
        MerchantRow(merchant: Merchant(id: UUID().uuidString, available: true, currency: "BRL", deliveryInfo: DeliveryInfo(type: "Delivery", fee: 120, timeMinMinutes: 55, timeMaxMinutes: 120), imageUrl: "logosgde/06448d05-5295-498d-bf4c-6fad4d37d69b_PAGUE_OJA03.png",  mainCategory: "Lanches", name: "Pague Menos - Av Cillos - Loja 03", userRating: 4.645, description: "Lanches do Dedao"))
    }
}
