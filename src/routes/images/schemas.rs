use serde::{Deserialize, Serialize};

#[derive(Serialize)]
pub struct Error {
    pub message: String,
}

#[derive(Serialize)]
pub struct Image {
    pub id: i64,
    pub url: String,
    pub rating: Rating,
    pub tags: Vec<String>,
}

#[derive(Deserialize, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum Rating {
    Safe,
    Suggestive,
    Borderline,
    Explicit,
}

impl Rating {
    pub fn from_string(string: &String) -> Result<Self, &'static str> {
        match string.to_lowercase().as_str() {
            "safe" => Ok(Self::Safe),
            "suggestive" => Ok(Self::Suggestive),
            "borderline" => Ok(Self::Borderline),
            "explicit" => Ok(Self::Explicit),
            _ => Err("The provided value is not a valid Rating enum value."),
        }
    }
}

#[derive(Serialize)]
pub struct PaginatedResponse<T: Serialize> {
    pub items: Vec<T>,
    pub count: i64,
}
