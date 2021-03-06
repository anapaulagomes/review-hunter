from .context import revas
from revas import UnauthorizedToken
from revas import endpoints
import os
import mock
from mock import ANY
import pytest
import requests


@pytest.fixture()
def reviewsapi():
    os.environ['UDACITY_AUTH_TOKEN'] = 'some auth token'
    yield revas.ReviewsAPI()


@mock.patch('revas.reviewsapi.requests.get')
def test_retrieve_certifications_list(mock_certifications, reviewsapi):
    expected_response = [{
                    'id': 0,
                    'status': 'applied',
                    'active': True,
                    'created_at': 'string',
                    'updated_at': 'string',
                    'waitlisted_at': 'string',
                    'certified_at': 'string',
                    'project_id': 0,
                    'grader_id': 0,
                    'trainings_count': 0,
                    'project': {
                      'id': 0,
                      'name': 'string',
                      'required_skills': 'string',
                      'awaiting_review_count': 0,
                      'hashtag': 'string',
                      'visible': True,
                      'audit_rubric_id': 0
                    }
                  }
                ]

    mock_certifications.return_value.ok = True
    mock_certifications.return_value.json.return_value = expected_response
    certifications_response = reviewsapi.certifications()

    mock_certifications.assert_called_once_with(endpoints.CERTIFICATIONS, headers=ANY)
    assert certifications_response == expected_response


@mock.patch('revas.reviewsapi.requests.get')
def test_retrieve_certified_languages_to_perform_reviews(mock_review_profile, reviewsapi):
    expected_languages_response = {'application': {'languages': ['en-us', 'zh-cn', 'pt-br']}}

    mock_review_profile.return_value.ok = True
    mock_review_profile.return_value.json.return_value = expected_languages_response
    languages_list = reviewsapi.certified_languages()

    mock_review_profile.assert_called_once_with(endpoints.REVIEWER, headers=ANY)
    assert languages_list == expected_languages_response


@mock.patch('revas.UnauthorizedToken')
@mock.patch('revas.reviewsapi.requests.get')
def test_unauthorized_url_access_when_try_access_to_certifications_list(mock_certifications, mock_http_error_handler, reviewsapi):
    mock_certifications.return_value.ok = False
    mock_certifications.return_value.json.side_effect = requests.exceptions.HTTPError()
    mock_http_error_handler.side_effect = UnauthorizedToken()

    with pytest.raises(UnauthorizedToken):
        reviewsapi.certifications()


@mock.patch('revas.reviewsapi.requests.get')
def test_should_throw_an_exception_when_status_code_is_different_of_2xx(mock_request, reviewsapi):
    http_error = requests.exceptions.HTTPError()
    mock_request.return_value.ok = False
    mock_request.return_value.raise_for_status.side_effect = http_error

    with pytest.raises(Exception):
        reviewsapi.certifications()


@mock.patch('revas.reviewsapi.requests.get')
def test_should_throw_an_exception_when_happens_a_network_problem(mock_request, reviewsapi):
    http_error = requests.exceptions.ConnectionError()
    mock_request.return_value.ok = False
    mock_request.return_value.raise_for_status.side_effect = http_error

    with pytest.raises(Exception):
        reviewsapi.certifications()


@mock.patch('revas.reviewsapi.requests.post')
def test_create_new_request_with_wanted_projects(mock_request, reviewsapi):
    fake_projects = {'projects':
                [{'project_id': 1, 'language': 'pt-br'},
                {'project_id': 2, 'language': 'pt-br'},
                {'project_id': 3, 'language': 'pt-br'}]}
    mock_request.return_value.ok = True

    response = reviewsapi.request_reviews(fake_projects)

    mock_request.assert_called_once_with(endpoints.NEW_SUBMISSION_REQUESTS, headers=ANY, json=fake_projects)
    assert response.status_code is not None


@mock.patch('revas.reviewsapi.requests.get')
def test_retrieve_the_number_of_current_assigned_projects(mock_assigned_count, reviewsapi):
    expected_assigned_count = {'assigned_count': 0}
    mock_assigned_count.return_value.ok = True
    mock_assigned_count.return_value.json.return_value = expected_assigned_count

    assigned_count_response = reviewsapi.assigned_count()

    mock_assigned_count.assert_called_once_with(endpoints.ASSIGNED_COUNT, headers=ANY)
    assert assigned_count_response == expected_assigned_count

    
@mock.patch('revas.reviewsapi.requests.get')
def test_get_the_active_submission_requests(mock_submission_requests, reviewsapi):
    expected_submission_requests_response = [{
        'id': 0,
        'user_id': 0,
        'status': 'available',
        'closed_at': 'string',
        'created_at': 'string',
        'submission_id': 0,
        'updated_at': 'string',
        'submission_request_projects': [{
            'project_id': 0,
            'language': 'en-us'
          }]
      }]
    mock_submission_requests.return_value.ok = True
    mock_submission_requests.return_value.json.return_value = expected_submission_requests_response

    submission_requests_response = reviewsapi.submission_requests()

    mock_submission_requests.assert_called_once_with(endpoints.SUBMISSION_REQUESTS, headers=ANY)
    assert submission_requests_response == expected_submission_requests_response
