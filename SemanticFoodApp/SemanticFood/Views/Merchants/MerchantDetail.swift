
import SwiftUI

struct MerchantDetail: View {
    var merchant: Merchant
    @StateObject private var model = MerchantsViewModel()
    
    var body: some View {
        let minTime = String(merchant.deliveryInfo?.timeMinMinutes ?? 0)
        let maxTime = String(merchant.deliveryInfo?.timeMaxMinutes ?? 0)
        let hasDeliveryInfo = merchant.deliveryInfo != nil
        let fullFee: Double = Double(merchant.deliveryInfo?.fee ?? 0) / 100
        
        ScrollView {
            HStack {
                VStack(alignment: .leading) {
                    Text(merchant.name)
                        .font(.title)
                        .bold()
                    HStack(spacing: 10) {
                        Text(merchant.mainCategory)
                            .foregroundStyle(.gray)
                        Text("*")
                            .foregroundStyle(.gray)
                        Text("X Km")
                            .foregroundStyle(.gray)
                        Text("*")
                            .foregroundStyle(.gray)
                        Text("$$$$")
                            .foregroundStyle(.gray)
                    }
                    .font(.system(size: 16))
                    .padding(.top, 01)
                    HStack {
                        Text("★ " + String(format: "%.2f", merchant.userRating))
                            .foregroundStyle(.gray)
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
                    }
                    .padding(.top, 10)
                    
                }
                .frame(
                    maxWidth: .infinity,
                    maxHeight: .infinity,
                    alignment: .topLeading
                )
                .padding(.top, 1)
                CircleImage(imageUrl: merchant.ifoodLogoUrl())
            }
            .padding()
            .frame(
                  minWidth: 0,
                  maxWidth: .infinity,
                  minHeight: 0,
                  maxHeight: .infinity,
                  alignment: .topLeading
            )
            VStack(alignment: .leading) {
                Text("Recomendados")
                    .font(.system(size: 28))
                    .bold()
                ForEach(model.recommendations) { merchant in
                    NavigationLink(destination: MerchantDetail(merchant: merchant)) {
                        MerchantRow(merchant: merchant)
                    }
                }
            }
            
            .padding()
            .frame(
                minWidth: 0,
                maxWidth: .infinity,
                minHeight: 0,
                maxHeight: .infinity,
                alignment: .topLeading
            )
        }
        .onAppear {
            loadRecommendations(merchantId: merchant.id)
        }
    }
    
    func loadRecommendations(merchantId: String) {
        Task {
           try await model.get_recommendations(merchantId: merchantId)
        }
    }
}

#Preview {
    MerchantDetail(merchant: Merchant(id: UUID().uuidString, available: true, currency: "BRL", deliveryInfo: DeliveryInfo(type: "Delivery", fee: 120, timeMinMinutes: 55, timeMaxMinutes: 120), imageUrl: "logosgde/06448d05-5295-498d-bf4c-6fad4d37d69b_PAGUE_OJA03.png",  mainCategory: "Lanches", name: "Pague Menos", userRating: 4.645, description: "Lanches do Dedao"))
}
