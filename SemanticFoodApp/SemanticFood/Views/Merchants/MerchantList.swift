import SwiftUI

struct MerchantList: View {
    var title: String
    var merchants: [Merchant]
    
    var body: some View {
        List(merchants) { merchant in
            NavigationLink {
                MerchantDetail(merchant: merchant)
            } label: {
                MerchantRow(merchant: merchant)
            }
        }
        .navigationTitle(title)
    }
}

#Preview {
    MerchantList(title: "Lojas", merchants: [Merchant]())
}
