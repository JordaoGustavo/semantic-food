//
//  CircleImage.swift
//  SemanticFood
//
//  Created by Gustavo Jordao on 08/05/24.
//

import SwiftUI

struct CircleImage: View {
    var imageUrl: String
        
    var body: some View {
        let image = AsyncImage(url: URL(string: imageUrl)) { phase in
            switch phase {
            case .empty:
                ProgressView()
            case .success(let image):
                image
                    .resizable()
                    .frame(width: 65, height: 65)
            case .failure:
                Image(systemName: "photo")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
            @unknown default:
                EmptyView()
            }
        }
        
        image.clipShape(Circle())
            .overlay {
                Circle().stroke(.white, lineWidth: 2)
            }
            .shadow(radius: 5)
            
    }
}

#Preview {
    CircleImage(imageUrl: "https://static.ifood-static.com.br/image/upload/t_thumbnail/logosgde/06448d05-5295-498d-bf4c-6fad4d37d69b_PAGUE_OJA03.png")
}
